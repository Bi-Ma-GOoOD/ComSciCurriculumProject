import fitz, re
from enum import Enum
from ..models import Enrollment, User, Course, Form, VerificationResult
from django.core.exceptions import ObjectDoesNotExist
from io import BytesIO
from ..minio_client import upload_to_minio, download_from_minio

class OCRService():
    class CheckType(Enum):
        INVALID = 0
        CRED_VALID = 1
        GRAD_VALID = 2
        
    def __init__(self):
        self.semester_mapping = {"Summer":0, "First":1, "Second":2}
        self.grade_mapping = {'A':4, 'B':3, 'B+':3.5, 'C':2, 'C+':2.5, 'D':1, 'D+':1.5, 'F':0} #NOTE: handle DecimalField
        
    def extract_text_from_file_path(self, file_path):
        with open(file_path, 'rb') as file:
            doc = fitz.open(file)
            text = ""
            for page in doc:
                text += page.get_text("text") + "\n"
            return text.split("\n")
        
    def extract_text_from_pdf(self, uploaded_file):
        file_stream = BytesIO(uploaded_file.read())  # โหลดไฟล์เข้า memory
        with fitz.open(stream=file_stream, filetype="pdf") as doc:
            text = "\n".join([page.get_text("text") for page in doc])  # ดึงข้อความจากทุกหน้า
        return text.split("\n")
        
    def get_valid_course(self, course, start_year):
        if '-' in course.course_id:
            _, course_year = course.course_id.split('-')
            course_year = int(course_year)
            return (start_year - 5) < course_year <= start_year
        return True
    
    def get_student_info(self, text):
        student_info = {}
        recent_year = None
        recent_semester = None
        
        for i, item in enumerate(text):
            match = re.match(r"\s*STUDENT ID\s+(\d{10})", item)
            if match:
                student_info["id"] = match.group(1)
            
            match = re.match(r"\s*NAME\s+(.+)", item)
            if match:
                student_info["name"] = match.group(1)
                
            match = re.match(r"\s*FACULTY OF\s+(.+)", item)
            if match:
                student_info["faculty"] = match.group(1)
            
            match = re.match(r"\s*FIELD OF STUDY\s+(.+)", item)
            if match:
                student_info["field"] = match.group(1)
                
            match = re.match(r"\s*DATE OF ADMISSION\s+(.+)", item)
            if match:
                student_info["start_year"] = int(match.group(1).split()[2]) + 543
            
            semester_match = re.match(r"\s*(First|Second)( Semester| Summer Session) (\d{4})", item)
            if semester_match:
                semester = self.semester_mapping.get(semester_match.group(1), None)
                year = int(semester_match.group(3)) + 543
                
                if not recent_year or (year > recent_year) or (semester > recent_semester):
                    recent_year = year
                    recent_semester = semester
                    
        if recent_year and recent_semester:
            student_info["recent_year"] = recent_year
            student_info["recent_semester"] = recent_semester
                
        return student_info
    
    def extract_receipt_info(self, text):
        receipt_info = {}
        text_str = " ".join(text)
        
        student_id_match = re.search(r"\b(\d{10})\b", " ".join(text))
        receipt_info["id"] = student_id_match.group(1) 

        name_index = text.index("STUDENT NAME") + 2 # +2 for ENG name
        receipt_info["name"] = text[name_index]
        
        academic_year_match = re.search(r"(\d{4}),\s*ภาค(?:ปลาย|ต้น)", " ".join(text))
        receipt_info["year"] = academic_year_match.group(1) 

        semester_match = re.search(r"(First|Second)( Semester| Summer Session)", " ".join(text))
        receipt_info["semester"] = self.semester_mapping.get(semester_match.group(1), None) 

        total_fee_match = re.search(r"รวม\s*/\s*TOTAL\s+([\d,]+.\d{2})", " ".join(text))
        receipt_info["total_fee"] = total_fee_match.group(1) 

        payment_keywords = {
            "Bank": "ธนาคาร",
            "Student Loan": "เงินกู้",
            "Cashier": "แคชเชียร์เช็ค",
            "Credit": "บัตรเครดิต",
            "Cash": "เงินสด",
            "Scholarship": "ทุนการศึกษา",
            "Org. Project": "ผ่านโครงการ"
        }

        found_payment_method = None
        for eng, thai in payment_keywords.items():
            if thai in text_str or eng in text_str:
                found_payment_method = eng
                break

        receipt_info["payment_method"] = found_payment_method

        return receipt_info
        
    def extract_semester(self, item):
        semester_match = re.match(r"(First|Second) Semester (\d{4})", item)
        summer_match = re.match(r"(First|Second)* Summer Session (\d{4})", item)
        
        if semester_match:
            term, year = semester_match.groups()
            return f"{1 if term == 'First' else 2}/{int(year) + 543}"
        elif summer_match:
            _, year = summer_match.groups()
            return f"0/{int(year) - 1 + 543}"
        return None
    
    #NOTE: Grading in Char , DONE   
    def extract_course_info(self, text, user):
        start_year = int(str(user.student_code)[:2])
        courses = {course.course_id: course for course in Course.objects.all() if self.get_valid_course(course, start_year)}
        count = 0
        current_semester = None

        i = 0
        while i < len(text):
            item = text[i].strip()
            
            semester = self.extract_semester(item)
            if semester:
                current_semester = semester

            # match course id and course name
            course_match = re.match(r"(\d{8})\s+(.+)", item) 
            if course_match and current_semester:
                course_id = course_match.group(1)

                matching_courses = [course for course in courses.values() if course.course_id.startswith(course_id)]
                
                if matching_courses:
                    selected_course = max(matching_courses, key=lambda c: int(c.course_id.split('-')[-1]) if '-' in c.course_id else 0)
                    course = selected_course
                else:
                    raise ValueError(f"course with {course_id} not found.") #NOTE: บางวิชาไม่มีในระบบ
                    
                # ถ้าไม่มีเกรดข้ามเรื่อยๆจนกว่าจะเจอเกรด
                grading = None
                j = i + 1
                while j < len(text):
                    next_item = text[j].strip()
                    if next_item in ['A', 'B', 'B+', 'C', 'C+', 'D', 'D+', 'F', 'P', 'NP', 'N']:
                        # grading = self.grade_mapping.get(next_item, -1) #NOTE: handle DecimalField
                        grading = next_item
                        break
                    j += 1  

                if grading:
                    s, y = current_semester.split('/')
                    if not Enrollment.objects.filter(
                        user_fk=user, 
                        course_fk=course,
                        semester=s, 
                        year=y
                    ).exists():
                        print(Enrollment.objects.create(
                            semester=s, 
                            year=y, 
                            grade=grading, 
                            user_fk=user, 
                            course_fk=course
                        ))
                        count += 1
            i += 1  
            
        print("Total courses:", count)
    
    def get_studentId_activity(self, text, uid):
        id_match = re.match(r".+\s+(\d{10})", text[1])
        if id_match:
            matched_uid = id_match.group(1)
            return matched_uid
        else:
            return None
    
    def is_valid_transcript(self, text):
        transcript_patterns = [
            r"KASETSART UNIVERSITY",
            r"THAILAND",
            r"STUDENT ID\s+(\d{10})",
            r"NAME\s+([A-Za-z.\s]+)",
            r"ID NO\.\s+([\d\s]+)",
            r"PLACE OF BIRTH\s+([A-Za-z]+)",
            r"DATE OF ADMISSION\s+([A-Za-z]+\s+\d{1,2},\s+\d{4})",
            r"FACULTY OF\s+([A-Za-z\s]+)",
            r"FIELD OF STUDY\s+([A-Za-z\s]+)",
            r"DEGREE CONFERRED\s+([A-Za-z.()\s]+)"
        ]
        
        text_str = " ".join(text)
        
        for pattern in transcript_patterns:
            if not re.search(pattern, text_str):
                return False
            
        return True
        
    def check_pass_activity(self, text):
        return True if "PASS" in text else False

    def is_valid_receipt_format(self, text):
        return bool(re.search(r"ใบเสร็จรับเงิน\.*", text[2]))

    def check_validation(self, files):
        try:
            """user = User.objects.create(
                email = "moradop.h@ku.th",
                password = "123456",
                name = "Moradop",
                student_code = "6510450861",
                role = "student"
            )
            form = Form.objects.create(
                form_type = Form.FormType.CREDIT_CHECK,
                user_fk = user
            )
            Form.objects.create(
                form_type = Form.FormType.GRADUATION_CHECK,
                user_fk = user
            )"""

            user = User.objects.get(user_id="e6c70c9292b547f19c2446e12df63004") #mock
            form = Form.objects.get(form_id="be12d9fb14de48de928dc867419a15b3") #mock

            response = {
                "transcript": {"valid": False, "message": ""},
                "activity": {"valid": False, "message": ""},
                "receipt": {"valid": False, "message": ""}
            }

            if files[0]:
                transcript = self.extract_text_from_pdf(files[0])
                st_info = self.get_student_info(transcript)
                
                if self.is_valid_transcript(transcript):
                    if st_info["id"] == user.student_code:
                        if st_info["field"].lower() == "computer science":
                            response["transcript"]["valid"] = True
                            self.extract_course_info(transcript, user)
                        else:
                            response["transcript"]["message"] = "Invalid field in transcript (should be 'Computer Science')."
                    else:
                        response["transcript"]["message"] = "Student ID in transcript does not match."
                else:
                    response["transcript"]["message"] = "Invalid transcript format."

            if files[1]:
                activity = self.extract_text_from_pdf(files[1])
                
                if self.get_studentId_activity(activity, user.student_code) == user.student_code:
                    response["activity"]["valid"] = True
                else:
                    response["activity"]["message"] = "Invalid or mismatched activity data."

            if files[2]:
                receipt = self.extract_text_from_pdf(files[2])
                receipt_info = self.extract_receipt_info(receipt)
                
                if self.is_valid_receipt_format(receipt):
                    if receipt_info["id"] == user.student_code:
                        response["receipt"]["valid"] = True
                    else:
                        response["receipt"]["message"] = "Receipt ID does not match student ID."
                else:
                    response["receipt"]["message"] = "Invalid receipt format."
            
            if any(file["valid"] for file in response.values()):
                check = self.CheckType.INVALID
                
                if form.form_type == Form.FormType.CREDIT_CHECK and response["transcript"]["valid"] and not response["activity"]["valid"] and not response["receipt"]["valid"]:
                    upload_to_minio(files[0], f"{user.student_code}/transcript.pdf")
                    check = self.CheckType.CRED_VALID
                    
                if form.form_type == Form.FormType.GRADUATION_CHECK and all(file["valid"] for file in response.values()):
                    if self.check_pass_activity(activity):
                        if receipt_info["year"] == st_info["recent_year"] and receipt_info["semester"] == st_info["recent_semester"]:
                            upload_to_minio(files[0], f"{form.form_id}/transcript.pdf")
                            upload_to_minio(files[1], f"{form.form_id}/activity.pdf")
                            upload_to_minio(files[2], f"{form.form_id}/receipt.pdf")
                            check = self.CheckType.GRAD_VALID
                        else:
                            response["receipt"]["message"] += "Invalid semester/year in receipt."
                    else:
                        response["activity"]["message"] += "Activity status is not PASS."
                    
                if check != self.CheckType.INVALID:
                    if check == self.CheckType.CRED_VALID:
                        VerificationResult.objects.create(
                            form_fk=form
                        )
                    elif check == self.CheckType.GRAD_VALID:
                        VerificationResult.objects.create(
                            activity_status=VerificationResult.VerificationResult.PASS,
                            fee_status=VerificationResult.VerificationResult.PASS,
                            form_fk=form
                        )
                    form.status = Form.FormStatus.READY_TO_CALC
                    form.save()
                    return {"status": "success", "message": "All files are valid."}
            return {
                "status": "failure",
                "message": "Some files failed validation.",
                "errors": response
            }
        except ObjectDoesNotExist as e:
            return {"status": "failure", "message": "User or form not found."}
    