from rest_framework.test import APITestCase

from main.models import Curriculum, Category, Subcategory, Course, Enrollment, Form
from main.utils import mock_data
from main.services import EducationEvaluationService, GradeVerificationService

class APICourseVerify(APITestCase) :
    def setUp(self) :
        self.gradeVerifyURL = '/api/credit-verify/'
        self.calculaterURL = '/api/calculate/'
        
        self.user, form, self.verificationResult = mock_data.mockUser('6510450000')
        
        form.form_type = Form.FormStatus.READY_TO_CALC
        form.save()
                
        self.curriculum = Curriculum.objects.get(curriculum_year=2565)
        
        self.category = Category.objects.order_by('category_name').get(category_name='หมวดวิชาเฉพาะ', curriculum_fk=self.curriculum.curriculum_id)
        self.subcategory = Subcategory.objects.order_by('subcategory_name').filter(category_fk=self.category.category_id).first()
        self.subjects = Course.objects.order_by('course_name_th').filter(subcategory_fk=self.subcategory.subcategory_id)[:2]
        
        self.enrollment = []
        for subject in self.subjects :
            self.enrollment.append(Enrollment.objects.create(
                semester=Enrollment.Semester.FIRST,
                year=2565,
                user_fk=self.user,
                course_fk=subject,
                grade='A',
            ))
            
        self.service = EducationEvaluationService()
        
    def test_api(self) :        
        calResponse = self.client.post(f'{self.calculaterURL}?uid={self.user.user_id}')
        response = self.client.get(self.gradeVerifyURL, {'uid': self.user.user_id})
        
        print()
        print('display calculating data:', calResponse.json())
        print('display calculated data:', response.json())
        
    def test_api_delete(self) :
        calResponse = self.client.post(f'{self.calculaterURL}?uid={self.user.user_id}')
        response = self.client.delete(f'{self.gradeVerifyURL}?uid={self.user.user_id}')
        
        print()
        print('display calculating data:', calResponse.json())
        print('display delete status:', response.json())
        
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(len(Enrollment.objects.filter(user_fk=self.user.user_id)), 0)
        self.assertEqual(Form.objects.get(user_fk=self.user.user_id).form_status, Form.FormStatus.DRAFT)