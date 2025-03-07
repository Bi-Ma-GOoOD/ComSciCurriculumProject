from typing import List
from django.test import TestCase

from main.services import CalculatorService
from main.models import Category, Curriculum, Subcategory, Course, Enrollment, User

class CalculateTestCase(TestCase) :
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
        self.cate2 = Category.objects.create(
            category_name='หมวดวิชาเฉพาะ',
            category_min_credit=88,
            curriculum_fk=self.cur1,
        )
        
        self.subcate1 = Subcategory.objects.create(
            subcategory_name='กลุ่มสาระภาษากับการสื่อสาร',
            subcateory_min_credit=13,
            category_fk=self.cate1,
        )
        self.subcate2 = Subcategory.objects.create(
            subcategory_name='กลุ่มสาระอยู่ดีมีสุข',
            subcateory_min_credit=3,
            category_fk=self.cate1,
        )
        self.subcate3 = Subcategory.objects.create(
            subcategory_name='วิชาแกน',
            subcateory_min_credit=12,
            category_fk=self.cate2,
        )
        
        self.c1 = Course.objects.create(
            course_id='01177111-65',
            credit=1,
            course_name_th='กรีฑาลู่-ลาน เพื่อสุขภาพ',
            course_name_en='Track and Field for Health',
            subcategory_fk=self.subcate2
        )
        self.c2 = Course.objects.create(
            course_id='01371101-65',
            credit=3,
            course_name_th='ภาษากับการสื่อสาร',
            course_name_en='English for Everyday Life',
            subcategory_fk=self.subcate1
        )
        self.c3 = Course.objects.create(
            course_id='01417112-65',
            credit=3,
            course_name_th='แคลคูลัส',
            course_name_en='Calculus',
            subcategory_fk=self.subcate3
        )
        
        # setup student enrollment
        self.st_enrollment1 = Enrollment.objects.create(
            semester=Enrollment.Semester.FIRST,
            year=2565,
            grade='F',
            user_fk=self.u,
            course_fk=self.c3,
        )
        self.st_enrollment2 = Enrollment.objects.create(
            semester=Enrollment.Semester.SECOND,
            year=2565,
            grade='B+',
            user_fk=self.u,
            course_fk=self.c3,
        )
        self.st_enrollment3 = Enrollment.objects.create(
            semester=Enrollment.Semester.FIRST,
            year=2566,
            grade='A',
            user_fk=self.u,
            course_fk=self.c3,
        )
        self.st_enrollment4 = Enrollment.objects.create(
            semester=Enrollment.Semester.FIRST,
            year=2565,
            grade='A',
            user_fk=self.u,
            course_fk=self.c2,
        )
        
    def test_calculate_nonduplicate_grade(self) :
        calculatorService = CalculatorService()
        
        enrollments = [self.st_enrollment2, self.st_enrollment4]
        calculatedEnrollments: List[Enrollment] = calculatorService.GPACalculate(enrollments)
        
        self.assertEqual(len(calculatedEnrollments), 2)
        self.assertAlmostEqual(calculatedEnrollments[0].totalGrade, 3.50)
        self.assertAlmostEqual(calculatedEnrollments[1].totalGrade, 4.00)
    
    def test_calculate_duplicate_grade(self) :
        calculatorService = CalculatorService()
        
        enrollments = [self.st_enrollment1, self.st_enrollment2, self.st_enrollment3]
        calculatedEnrollments: List[Enrollment] = calculatorService.GPACalculate(enrollments)
        
        self.assertEqual(len(calculatedEnrollments), 1)
        self.assertAlmostEqual(calculatedEnrollments[0].totalGrade, 2.50)
        