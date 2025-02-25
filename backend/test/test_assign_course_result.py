from django.test import TestCase

from main.utils.mock_data import *
from main.services import EducationEvaluationService

class AssignResult(TestCase) :
    def setUp(self) :
        self.calculator = EducationEvaluationService()
        
        self.student = mockUser()
        
        self.curriculum = mockCurriculum()
        self.categories = mockCategories(self.curriculum)
        
        self.subcategories = mockSubcategories(self.categories[0], [('X', 4)])
        
        self.courses = mockCourses(self.subcategories[0], [3, 2, 1])
        
        enrollments = [(c, 'A', 2565) for c in self.courses]
        enrollments.append((self.courses[0], 'F', 2566))
        self.studiedCourse = mockEnrollments(self.student, enrollments)

    def test_checking_result(self) :
        result = self.calculator.verify(self.curriculum, self.studiedCourse, self.categories, self.subcategories, self.courses)
        print(result.data)