from typing import List
from django.test import TestCase

from main.services import CalculatorService
from main.models import Category, Curriculum, Subcategory, Course, Enrollment, User, SubcategoryDetails

class MappingTest(TestCase) :
    def setUp(self):
        # setup user
        self.u = User.objects.create(
            email='abc@gmail.com',
            password='1234',
            name='doe',
            student_code='6510450569',
            role=User.Role.STUDENT,
        )
        
        # setup curriculum
        self.cur1 = Curriculum.objects.create(
            curriculum_name='หลักสูตรวิทยาศาสตรบัณฑิต สาขาวิชาวิทยาการคอมพิวเตอร์',
            total_credit=124,
            curriculum_year=2565,
        )
        
        self.cate1 = Category.objects.create(
            category_name='หมวดวิชาศึกษาทั่วไป',
            category_min_credit=30,
            curriculum_fk=self.cur1,
        )
        
        self.subcate1 = Subcategory.objects.create(
            subcategory_name='a',
            subcateory_min_credit=4,
            category_fk=self.cate1,
        )
        
        self.c1 = Course.objects.create(
            course_id='course a',
            credit=2,
            subcategory_fk=self.subcate1
        )
        self.c2 = Course.objects.create(
            course_id='course b',
            credit=3,
            subcategory_fk=self.subcate1
        )
        self.c3 = Course.objects.create(
            course_id='course c',
            credit=1,
            subcategory_fk=self.subcate1
        )
        
        # setup student enrollment
        self.st_enrollment1 = Enrollment.objects.create(
            semester=Enrollment.Semester.FIRST,
            year=2565,
            grade='B',
            user_fk=self.u,
            course_fk=self.c1,
        )
        self.st_enrollment2 = Enrollment.objects.create(
            semester=Enrollment.Semester.SECOND,
            year=2565,
            grade='B+',
            user_fk=self.u,
            course_fk=self.c2,
        )
        self.st_enrollment3 = Enrollment.objects.create(
            semester=Enrollment.Semester.FIRST,
            year=2566,
            grade='A',
            user_fk=self.u,
            course_fk=self.c3,
        )
        
        self.calculator = CalculatorService()
        
    def test_mapping_course_to_curriculum(self) :
        courses = [self.st_enrollment1, self.st_enrollment2, self.st_enrollment3]
        calculated_course = self.calculator.GPACalculate(courses)
        
        subcategory = [self.subcate1]
        
        mappingResult: List[SubcategoryDetails] = self.calculator.map(subcategory, calculated_course)
        
        freeElective = mappingResult['free elective']
        categorizedCourse = mappingResult['categorize course']
        
        self.assertEqual(len(freeElective), 1)
        self.assertEqual(len(categorizedCourse), 1)

        self.assertEqual(len(categorizedCourse[0]['matchEnrollment']), 2)
        
    def test_mapping_with_less_than_creadit(self) :
        courses = [self.st_enrollment1]
        
        subcategory = [self.subcate1]
        
        mappingResult: List[SubcategoryDetails] = self.calculator.map(subcategory, self.calculator.GPACalculate(courses))
        
        freeElective = mappingResult['free elective']
        categorizedCourse = mappingResult['categorize course']
        
        self.assertEqual(len(freeElective), 0)
        self.assertEqual(len(categorizedCourse), 1)

        self.assertEqual(len(categorizedCourse[0]['matchEnrollment']), 1)
        
    def test_mapping_with_equal_creadit(self) :
        courses = [self.st_enrollment2, self.st_enrollment3]
        
        subcategory = [self.subcate1]
        
        mappingResult: List[SubcategoryDetails] = self.calculator.map(subcategory, self.calculator.GPACalculate(courses))
        
        freeElective = mappingResult['free elective']
        categorizedCourse = mappingResult['categorize course']
        
        self.assertEqual(len(freeElective), 0)
        self.assertEqual(len(categorizedCourse), 1)

        self.assertEqual(len(categorizedCourse[0]['matchEnrollment']), 2)
        
    def test_mapping_with_more_than_creadit_and_fit_divided(self) :
        self.c1.credit = 2
        self.c2.credit = 1
        self.c3.credit = 3
        
        courses = [self.st_enrollment1, self.st_enrollment2, self.st_enrollment3]
        
        subcategory = [self.subcate1]
        
        mappingResult: List[SubcategoryDetails] = self.calculator.map(subcategory, self.calculator.GPACalculate(courses))
        
        freeElective = mappingResult['free elective']
        categorizedCourse = mappingResult['categorize course']
        
        self.assertEqual(len(freeElective), 1)
        self.assertEqual(len(categorizedCourse), 1)

        self.assertEqual(len(categorizedCourse[0]['matchEnrollment']), 2)
        
        self.assertEqual(freeElective[0].enrollment.course_fk.course_id, 'course a')

    def test_mapping_with_more_than_creadit_and_unfit_divided(self) :
        self.c1.credit = 3
        self.c2.credit = 2
        self.c3.credit = 3
        
        courses = [self.st_enrollment1, self.st_enrollment2, self.st_enrollment3]
        
        subcategory = [self.subcate1]
        
        mappingResult: List[SubcategoryDetails] = self.calculator.map(subcategory, self.calculator.GPACalculate(courses))
        
        freeElective = mappingResult['free elective']
        categorizedCourse = mappingResult['categorize course']
        
        self.assertEqual(len(freeElective), 1)
        self.assertEqual(len(categorizedCourse), 1)

        self.assertEqual(len(categorizedCourse[0]['matchEnrollment']), 2)
        
        self.assertIn(freeElective[0].enrollment.course_fk.course_id, ['course a', 'course c'])