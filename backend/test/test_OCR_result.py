from django.test import TestCase

from main.utils.mock_data import *
from main.services import OCRService
from django.conf import settings

class OCRResult(TestCase):
    def setUp(self):
        self.ocr = OCRService()
        self.grade_text = self.ocr.extract_text_from_file_path(settings.BASE_DIR/"main/utils/OCR_transcript_test.pdf")
        self.activity_text = self.ocr.extract_text_from_file_path(settings.BASE_DIR/"main/utils/activity_transcript_test.pdf")
        self.invoice_text = self.ocr.extract_text_from_file_path(settings.BASE_DIR/"main/utils/invoice_test.pdf")
        self.soodlor = User.objects.create(
            email = "soodlorlnwza@gmail.com",
            password = "lorpainhai081",
            name = "soodlor mawa",
            student_code = "6510450861",
            role = "student"
        )
    def test_ocr(self):
        print(self.grade_text)
        print("==============================================================")
        print(self.activity_text)
        print("==============================================================")
        print(self.invoice_text)
        
    def test_activity_status(self):
        print("activity status: ", self.ocr.get_studentId_activity(self.activity_text, "6510450861"))
        
    def test_student_info(self):
        print(self.ocr.get_student_info(self.grade_text))
    
    def test_is_valid_transcript(self):
        print(self.ocr.is_valid_transcript(self.grade_text))
        
    # def test_course_info(self):
    #     print(self.ocr.extract_course_info(self.grade_text, self.soodlor))
    
    def test_receipt_info(self):
        print(self.ocr.extract_receipt_info(self.invoice_text))
    