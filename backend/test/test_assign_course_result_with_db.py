from django.test import TestCase
from django.conf import settings
import pytest

from main.models import Curriculum, Category, Subcategory, Course, Enrollment, VerificationResult, Form
from main.utils import mock_data
from main.services import EducationEvaluationService
from main.signals import initialize_curriculum_data

class AssignResultWithDB(TestCase) :
    def setUp(self) :        
        user = mock_data.mockUser()
        form = Form.objects.create(            
            user_fk = user,
        )
        verificationResult = VerificationResult.objects.create(
            form_fk = form
        )
        
        self.curriculum = Curriculum.objects.get(curriculum_year=2565)
        
        
        self.category = Category.objects.order_by('category_name').get(category_name='หมวดวิชาเฉพาะ', curriculum_fk=self.curriculum.curriculum_id)
        self.subcategory = Subcategory.objects.order_by('subcategory_name').filter(category_fk=self.category.category_id).first()
        self.subjects = Course.objects.order_by('course_name_th').filter(subcategory_fk=self.subcategory.subcategory_id)[:2]
        
        self.enrollment = []
        for subject in self.subjects :
            self.enrollment.append(Enrollment.objects.create(
                semester=Enrollment.Semester.FIRST,
                year=2565,
                user_fk=user,
                course_fk=subject,
                grade='A',
            ))
            
        self.service = EducationEvaluationService()
        
    def test_func(self) :
        print('self.category', self.category)
        print('self.subcategory', self.subcategory)
         
        result = self.service.verify(curriculum=self.curriculum, enrollments=self.enrollment)
        print(result.data)