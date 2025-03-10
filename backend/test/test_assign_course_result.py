from django.test import TestCase

from main.utils.mock_data import *
from main.services import EducationEvaluationService

class AssignResult(TestCase) :
    def setUp(self) :
        self.calculator = EducationEvaluationService()
        
        self.student = mockUser()
        
        self.curriculum = mockCurriculum()
        self.categories = mockCategories(self.curriculum)
        
        self.subcategories = mockSubcategories(self.categories[0])

    # def test_checking_result(self) :
    #     self.courses = mockCourses(self.subcategories[0], [3, 1])
        
    #     # enrollments = [(c, 'A', 2565) for c in self.courses[]]
    #     enrollments = [(self.courses[0], 'A', 2565)]
    #     enrollments.append((self.courses[1], 'A', 2566))
    #     self.studiedCourse = mockEnrollments(self.student, enrollments)
        
    #     result = self.calculator.verify(self.curriculum, self.studiedCourse, self.categories, self.subcategories, self.courses)
    #     with open('output.txt', 'w', encoding='utf-8') as f :
    #         f.write(str(result.data))

    def test_checking_result_with_norm_complete(self) :
        self.courses = mockCourses(self.subcategories[0], [4, 3])
        
        # enrollments = [(c, 'A', 2565) for c in self.courses[]]
        enrollments = [(self.courses[0], 'A', 2565)]
        enrollments.append((self.courses[1], 'A', 2566))
        self.studiedCourse = mockEnrollments(self.student, enrollments)
        
        result = self.calculator.verify(self.curriculum, self.studiedCourse, self.categories, self.subcategories, self.courses, isTesting=True)
        self.assertTrue(result['is_complete'].value)
        
    def test_checking_result_with_F_subject(self) :
        self.courses = mockCourses(self.subcategories[0], [4, 3])
        
        # enrollments = [(c, 'A', 2565) for c in self.courses[]]
        enrollments = [(self.courses[0], 'A', 2565)]
        enrollments.append((self.courses[1], 'F', 2566))
        self.studiedCourse = mockEnrollments(self.student, enrollments)
        
        result = self.calculator.verify(self.curriculum, self.studiedCourse, self.categories, self.subcategories, self.courses, isTesting=True)
        
        self.assertFalse(result['is_complete'].value)
        
    def test_checking_result_with_total_gpax_under_c(self) :
        self.courses = mockCourses(self.subcategories[0], [4, 3])
        
        # enrollments = [(c, 'A', 2565) for c in self.courses[]]
        enrollments = [(self.courses[0], 'C', 2565)]
        enrollments.append((self.courses[1], 'D+', 2566))
        self.studiedCourse = mockEnrollments(self.student, enrollments)
        
        result = self.calculator.verify(self.curriculum, self.studiedCourse, self.categories, self.subcategories, self.courses, isTesting=True)

        self.assertFalse(result['is_complete'].value)

    def test_checking_result_with_total_credit_less_than_require(self) :
        self.courses = mockCourses(self.subcategories[0], [3, 1])
        
        # enrollments = [(c, 'A', 2565) for c in self.courses[]]
        enrollments = [(self.courses[0], 'A', 2565)]
        enrollments.append((self.courses[1], 'A', 2566))
        self.studiedCourse = mockEnrollments(self.student, enrollments)
        
        result = self.calculator.verify(self.curriculum, self.studiedCourse, self.categories, self.subcategories, self.courses, isTesting=True)

        self.assertFalse(result['is_complete'].value)

    def test_checking_result_with_I_or_N_grade(self) :
        # TODO resolve prsentaton of grade
        self.courses = mockCourses(self.subcategories[0], [3, 1, 1, 2])
        
        # enrollments = [(c, 'A', 2565) for c in self.courses[]]
        enrollments = [(self.courses[0], 'A', 2565)]
        enrollments.append((self.courses[1], 'A', 2566))
        enrollments.append((self.courses[2], 'I', 2566))
        enrollments.append((self.courses[3], 'N', 2566))
        self.studiedCourse = mockEnrollments(self.student, enrollments)
        
        result = self.calculator.verify(self.curriculum, self.studiedCourse, self.categories, self.subcategories, self.courses, isTesting=True)
            
        self.assertFalse(result['is_complete'].value)
        
    def test_checking_result_with_W_grade_and_pass_requirement(self) :
        self.courses = mockCourses(self.subcategories[0], [4, 3, 1])
        
        # enrollments = [(c, 'A', 2565) for c in self.courses[]]
        enrollments = [(self.courses[0], 'A', 2565)]
        enrollments.append((self.courses[1], 'A', 2566))
        enrollments.append((self.courses[2], 'W', 2566))
        self.studiedCourse = mockEnrollments(self.student, enrollments)
        
        result = self.calculator.verify(self.curriculum, self.studiedCourse, self.categories, self.subcategories, self.courses, isTesting=True)
            
        self.assertTrue(result['is_complete'].value)
        
    def test_checking_result_with_W_grade_and_not_pass_requirement(self) :
        self.courses = mockCourses(self.subcategories[0], [4, 3, 1])
        
        # enrollments = [(c, 'A', 2565) for c in self.courses[]]
        enrollments = [(self.courses[0], 'A', 2565)]
        enrollments.append((self.courses[1], 'W', 2566))
        self.studiedCourse = mockEnrollments(self.student, enrollments)
        
        result = self.calculator.verify(self.curriculum, self.studiedCourse, self.categories, self.subcategories, self.courses, isTesting=True)
            
        self.assertFalse(result['is_complete'].value)
        