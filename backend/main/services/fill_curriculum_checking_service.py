import os
import fitz  # PyMuPDF
import uuid
import qrcode
from io import BytesIO
from datetime import datetime
from urllib.parse import urlparse
from django.conf import settings
from django.db.models import Avg, Sum, F
from main.models import Enrollment, User, Course, Curriculum, Category, Subcategory
from main.minio_client import minio_client, upload_to_minio, generate_presigned_url

FONT_PATH = os.path.join(settings.BASE_DIR, 'main', 'utils', 'font', 'Sarabun.ttf')

class FillCurriculumCheckingService:
    
    def __init__(self):
        self.template_dir = os.path.join(settings.BASE_DIR, 'main', 'utils')
        
    def _get_template_paths(self, curriculum_year):
        """
        Returns a dictionary of available template paths for different curriculum years
        """
        return {
            "2560": os.path.join(self.template_dir, f"แบบตรวจสอบหลักสูตรวิทยาศาสตรบัณฑิต_25{curriculum_year}.pdf"),
            "2565": os.path.join(self.template_dir, f"แบบตรวจสอบหลักสูตรวิทยาศาสตรบัณฑิต_25{curriculum_year}.pdf")
        }
    
    def _get_curriculum_year(self, student_code):
        """
        Determine the curriculum year based on student's entry year
        """
        try:
            entry_year = int(student_code[:2])
                
            base_year = 60  # Starting curriculum year
            interval = 5    # Curriculum updates every 5 years
                
            curriculum_year = base_year + ((entry_year - base_year) // interval) * interval
            return str(curriculum_year)
        except (ValueError, TypeError):
            return "65"  # Default to 2565 curriculum
    
    def _map_category_type(self, category_name):
        """
        Map category names to standardized types used in the PDF template
        """
        category_name = category_name.lower()
        
        category_mappings = {
            "general": ["general", "ศึกษาทั่วไป"],
            "core": ["core", "แกน"],
            "required": ["required", "บังคับ"],
            "elective": ["elective", "เลือก"],
            "free": ["free", "เสรี"]
        }
        
        for category, keywords in category_mappings.items():
            if any(keyword in category_name for keyword in keywords):
                return category
        
        return "free"  # Default to free elective
    
    def _prepare_enrollment_data(self, enrollments):
        """
        Organize enrollment data by category for PDF filling
        """
        enrollment_data = {
            "general": [],
            "core": [],
            "required": [],
            "elective": [],
            "free": []
        }
        
        for enrollment in enrollments:
            course = enrollment.course_fk
            subcategory = course.subcategory_fk
            category = subcategory.category_fk if subcategory else None
            
            # Determine category type
            category_type = "free"
            if category:
                category_type = self._map_category_type(category.category_name)
            
            course_info = {
                'course_id': course.course_id,
                'course_name': course.course_name_th,
                'credits': course.credit,
                'semester': enrollment.semester,
                'year': enrollment.year,
                'grade': enrollment.grade
            }
            
            enrollment_data[category_type].append(course_info)
        
        return enrollment_data
    
    
    
    
    
    def generate_filled_form(self, uid, template_version="2565"):
        """
        Generate filled curriculum checking form with flexible template selection
        
        Parameters:
        - uid: User ID
        - template_version: Version of the template to use (default: 2565)
        """
        # Get student data
        student = User.objects.get(user_id=uid)
        
        # Get enrollment data 
        enrollments = Enrollment.objects.filter(user_fk=uid).select_related(
            'course_fk', 
            'course_fk__subcategory_fk', 
            'course_fk__subcategory_fk__category_fk'
        )
        
        student_code = student.student_code
        curriculum_year = self._get_curriculum_year(student_code)
        
        # Select template paths
        template_paths = self._get_template_paths(curriculum_year)
        template_path = template_paths.get(template_version, template_paths["2565"])
        
        # Open the PDF template
        doc = fitz.open(template_path)
        
        # Prepare enrollment data
        enrollment_data = self._prepare_enrollment_data(enrollments)
        
        # Fill student information
        page = doc[0]  # First page
        
        # Dynamic template filling based on version
        if template_version == "2565":
            self._fill_2565_template(page, student, enrollment_data)
        else:
            self._fill_2560_template(page, student, enrollment_data)
        
        # Calculate GPA and total credits
        total_credits, gpa = self._calculate_academic_summary(enrollments)
        
        # Fill summary information on last page
        last_page = doc[-1]
        rect_credits = fitz.Rect(110, 597, 150, 615)
        last_page.insert_textbox(rect_credits, str(total_credits), fontname="THSarabun", fontfile=FONT_PATH, fontsize=10)
        
        rect_gpa = fitz.Rect(320, 597, 370, 615) 
        last_page.insert_textbox(rect_gpa, f"{gpa:.2f}", fontname="THSarabun", fontfile=FONT_PATH, fontsize=10)
        
        # Save to BytesIO
        output_buffer = BytesIO()
        doc.save(output_buffer)
        output_buffer.seek(0)
        
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{student_code}_curriculum_checking_25{curriculum_year}_{timestamp}.pdf"
        
        return output_buffer, filename
    
    def _fill_2565_template(self, page, student, enrollment_data):
        """
        Fill the 2565 curriculum template specific details
        """
        # Student name field
        rect_name = fitz.Rect(100, 80, 550, 100)
        page.insert_textbox(rect_name, student.name, fontname="THSarabun", fontfile=FONT_PATH, fontsize=12)
        
        # Student code field
        rect_id = fitz.Rect(480, 80, 550, 100)
        page.insert_textbox(rect_id, student.student_code, fontname="THSarabun", fontfile=FONT_PATH, fontsize=12)
        
        # Specific section filling for 2565 template
        sections = {
            "general": {"y_start": 100, "increments": [120, 170, 230]},
            "core": {"y_start": 480, "increments": [20]}
        }
        
        for category, section_info in sections.items():
            y_offset = section_info["y_start"]
            increment = section_info["increments"][0]
            
            for course in enrollment_data.get(category, []):
                # Course ID column
                rect_id = fitz.Rect(50, y_offset, 100, y_offset + increment)
                page.insert_textbox(rect_id, course.get('course_id', ''), fontname="THSarabun", fontfile=FONT_PATH, fontsize=10)
                
                # Course name column
                rect_name = fitz.Rect(150, y_offset, 300, y_offset + increment)
                page.insert_textbox(rect_name, course.get('course_name', ''), fontname="THSarabun", fontfile=FONT_PATH, fontsize=10)
                
                # Credits column
                rect_credits = fitz.Rect(350, y_offset, 400, y_offset + increment)
                page.insert_textbox(rect_credits, str(course.get('credits', '')), fontname="THSarabun", fontfile=FONT_PATH, fontsize=10)
                
                # Semester/Year column
                rect_semester = fitz.Rect(400, y_offset, 450, y_offset + increment)
                semester_text = f"{course.get('semester', '')}/{course.get('year', '')}"
                page.insert_textbox(rect_semester, semester_text, fontname="THSarabun", fontfile=FONT_PATH, fontsize=10)
                
                # Grade column
                rect_grade = fitz.Rect(460, y_offset, 500, y_offset + increment)
                page.insert_textbox(rect_grade, course.get('grade', ''), fontname="THSarabun", fontfile=FONT_PATH, fontsize=10)
                
                y_offset += increment
    
    # def _fill_2560_template(self, page, student, enrollment_data):
    #     """
    #     Fill the 2565 curriculum template specific details
    #     """
    #     # Student name field
    #     rect_name = fitz.Rect(250, 50, 500, 90)
    #     page.insert_textbox(rect_name, student.name, fontname="THSarabun", fontfile=FONT_PATH, fontsize=12)
        
    #     # Student code field
    #     rect_id = fitz.Rect(450, 50, 550, 90)
    #     page.insert_textbox(rect_id, student.student_code, fontname="THSarabun", fontfile=FONT_PATH, fontsize=12)
        
    #     # Specific section filling for 2565 template
    #     sections = {
    #         "general": {"y_start": 100, "increments": [120, 170, 230]},
    #         "core": {"y_start": 480, "increments": [20]}
    #     }
        
    #     for category, section_info in sections.items():
    #         y_offset = section_info["y_start"]
    #         increment = section_info["increments"][0]
            
    #         for course in enrollment_data.get(category, []):
    #             # Course ID column
    #             rect_id = fitz.Rect(50, y_offset, 100, y_offset + increment)
    #             page.insert_textbox(rect_id, course.get('course_id', ''), fontname="THSarabun", fontfile=FONT_PATH, fontsize=10)
                
    #             # Course name column
    #             rect_name = fitz.Rect(150, y_offset, 300, y_offset + increment)
    #             page.insert_textbox(rect_name, course.get('course_name', ''), fontname="THSarabun", fontfile=FONT_PATH, fontsize=10)
                
    #             # Credits column
    #             rect_credits = fitz.Rect(350, y_offset, 400, y_offset + increment)
    #             page.insert_textbox(rect_credits, str(course.get('credits', '')), fontname="THSarabun", fontfile=FONT_PATH, fontsize=10)
                
    #             # Semester/Year column
    #             rect_semester = fitz.Rect(400, y_offset, 450, y_offset + increment)
    #             semester_text = f"{course.get('semester', '')}/{course.get('year', '')}"
    #             page.insert_textbox(rect_semester, semester_text, fontname="THSarabun", fontfile=FONT_PATH, fontsize=10)
                
    #             # Grade column
    #             rect_grade = fitz.Rect(460, y_offset, 500, y_offset + increment)
    #             page.insert_textbox(rect_grade, course.get('grade', ''), fontname="THSarabun", fontfile=FONT_PATH, fontsize=10)
                
    #             y_offset += increment
    
    def _calculate_academic_summary(self, enrollments):
        """
        Calculate total credits and GPA from enrollments
        """
        grade_points = {
            'A': 4.0, 'B+': 3.5, 'B': 3.0, 'C+': 2.5, 
            'C': 2.0, 'D+': 1.5, 'D': 1.0, 'F': 0.0
        }
        
        total_grade_points = 0
        total_credits = 0
        
        for enrollment in enrollments:
            course = enrollment.course_fk
            grade = enrollment.grade
            
            if grade in grade_points:
                total_grade_points += course.credit * grade_points[grade]
                total_credits += course.credit
        
        gpa = total_grade_points / total_credits if total_credits > 0 else 0.0
        
        return total_credits, gpa
    
    def generate_and_upload(self, uid, template_version="2565"):
        """
        Generate a filled PDF form and upload it to MinIO
        Also generate a separate QR code image
        
        Parameters:
        - uid: UUID of the student
        - template_version: Version of the template to use
        
        Returns:
        - PDF download URL
        - PDF filename
        - QR code download URL (optional)
        - QR code filename (optional)
        """
        # Generate PDF buffer and filename
        pdf_buffer, pdf_filename = self.generate_filled_form(uid, template_version)
        
        # Ensure buffer is at the start
        pdf_buffer.seek(0)
        
        # Set content type 
        pdf_content_type = 'application/pdf'
        
        # Create a new BytesIO with the PDF content
        pdf_bytes = BytesIO(pdf_buffer.read())
        pdf_buffer.seek(0)  # Reset buffer for potential further use
        
        # Upload to MinIO
        try:
            minio_client.put_object(
                settings.MINIO_BUCKET,
                pdf_filename,
                pdf_bytes,
                length=len(pdf_bytes.getvalue()),
                content_type=pdf_content_type
            )
            print("PDF uploaded to MinIO successfully")
        except Exception as e:
            print(f"Error uploading PDF to MinIO: {e}")
            return None, pdf_filename, None, None
        
        # Generate a presigned URL for PDF download
        pdf_download_url = generate_presigned_url(pdf_filename)
        
        # Generate QR Code
        qr_buffer, qr_filename = self.generate_download_qr_code(pdf_download_url)
        
        # Ensure QR buffer is at the start
        qr_buffer.seek(0)
        
        # Set QR code content type
        qr_content_type = 'image/png'
        
        # Create a new BytesIO with the QR code content
        qr_bytes = BytesIO(qr_buffer.read())
        qr_buffer.seek(0)  # Reset buffer for potential further use
        
        # Upload QR code to MinIO
        try:
            minio_client.put_object(
                settings.MINIO_BUCKET,
                qr_filename,
                qr_bytes,
                length=len(qr_bytes.getvalue()),
                content_type=qr_content_type
            )
            print("QR code uploaded to MinIO successfully")
            
            # Generate presigned URL for QR code
            qr_download_url = generate_presigned_url(qr_filename)
            
            return pdf_download_url, pdf_filename, qr_download_url, qr_filename
        
        except Exception as e:
            print(f"Error uploading QR code to MinIO: {e}")
            return pdf_download_url, pdf_filename, None, None
    
    
    def generate_download_qr_code(self, download_url, size=10):
        """
        Generate a QR code image for the download URL
        
        Parameters:
        - download_url: URL to embed in the QR code
        - size: Box size of QR code (default 10)
        
        Returns:
        - BytesIO buffer containing QR code PNG image
        - Filename for the QR code
        """
        # Create QR code instance
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=size,
            border=4,
        )
        
        # Truncate URL to remove query parameters if needed
        # This ensures we have a clean URL for the QR code
        parsed_url = urlparse(download_url)
        clean_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
        
        # Add download URL to QR code
        qr.add_data(clean_url)
        qr.make(fit=True)
        
        # Create an image from the QR code
        qr_img = qr.make_image(fill_color="black", back_color="white")
        
        # Save to BytesIO buffer
        qr_buffer = BytesIO()
        qr_img.save(qr_buffer, format="PNG")
        qr_buffer.seek(0)
        
        # Generate filename based on the original filename
        try:
            # Try to extract filename from the URL path
            original_filename = os.path.basename(parsed_url.path)
            filename = f"qr_{original_filename}.png"
        except Exception:
            # Fallback to timestamp-based filename
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = f"download_qr_{timestamp}.png"
        
        return qr_buffer, filename