from django.test import TestCase
from tempfile import NamedTemporaryFile
import json
import os
from main.models import Curriculum, Category, Subcategory, Course
from main.signals import import_course_from_json

class TestImportFunctions(TestCase):
    """Test the import functions"""
    
    def setUp(self):
        """Run before each test to ensure a clean database state"""
        # Clear all existing courses to avoid conflicts
        Course.objects.all().delete()
        Subcategory.objects.all().delete()
        Category.objects.all().delete()
        Curriculum.objects.all().delete()
    
    def create_temp_json_file(self, data, prefix):
        """Helper to create a temporary JSON file with the given data"""
        temp_file = NamedTemporaryFile(prefix=prefix, suffix='.json', delete=False)
        temp_file.write(json.dumps(data).encode('utf-8'))
        temp_file.close()
        return temp_file.name
    
    def test_import_course_from_json(self):
        """Test importing courses from JSON file"""
        # Create test curriculum, category and subcategory first
        curriculum = Curriculum.objects.create(
            curriculum_name="Test Curriculum",
            total_credit=130,
            curriculum_year=2560
        )
        
        category = Category.objects.create(
            curriculum_fk=curriculum,
            category_name="หมวดวิชาเฉพาะ",
            category_min_credit=94
        )
        
        subcategory = Subcategory.objects.create(
            category_fk=category,
            subcategory_name="วิชาแกน",
            subcateory_min_credit=15
        )
        
        # Create test course data
        course_data = [
            {
                "str": 60,
                "field": "เฉพาะ",
                "tag": "แกน",
                "code": "01418112-60",
                "eng_name": "Computer Programming",
                "thai_name": "การเขียนโปรแกรมคอมพิวเตอร์",
                "credit": 3,
                "condition": ""
            }
        ]
        
        # Create temporary file
        temp_file = self.create_temp_json_file(course_data, "course_")
        
        try:
            # Call the import function
            import_course_from_json(temp_file)
            
            # Check course was created correctly
            self.assertEqual(Course.objects.count(), 1)
            
            # Check course details
            course = Course.objects.first()
            self.assertEqual(course.course_id, "01418112-60")
            self.assertEqual(course.course_name_en, "Computer Programming")
            self.assertEqual(course.course_name_th, "การเขียนโปรแกรมคอมพิวเตอร์")
            self.assertEqual(course.credit, 3)
            self.assertEqual(course.subcategory_fk, subcategory)
        finally:
            # Clean up
            os.unlink(temp_file)
    
    def test_import_course_with_non_exact_year(self):
        """Test importing a course with a year that doesn't exactly match a curriculum"""
        # Create test curriculum
        curriculum_2560 = Curriculum.objects.create(
            curriculum_name="Curriculum 2560",
            total_credit=130,
            curriculum_year=2560
        )
        
        curriculum_2565 = Curriculum.objects.create(
            curriculum_name="Curriculum 2565",
            total_credit=128,
            curriculum_year=2565
        )
        
        # Create categories and subcategories
        category_2560 = Category.objects.create(
            curriculum_fk=curriculum_2560,
            category_name="หมวดวิชาเฉพาะ",
            category_min_credit=94
        )
        
        category_2565 = Category.objects.create(
            curriculum_fk=curriculum_2565,
            category_name="หมวดวิชาเฉพาะ",
            category_min_credit=92
        )
        
        subcategory_2560 = Subcategory.objects.create(
            category_fk=category_2560,
            subcategory_name="วิชาแกน",
            subcateory_min_credit=15
        )
        
        subcategory_2565 = Subcategory.objects.create(
            category_fk=category_2565,
            subcategory_name="วิชาแกน",
            subcateory_min_credit=14
        )
        
        # Create test course data for year 63 (should match with 2560 curriculum)
        course_data = [
            {
                "str": 63,
                "field": "เฉพาะ",
                "tag": "แกน",
                "code": "01418112-63",
                "eng_name": "Computer Programming",
                "thai_name": "การเขียนโปรแกรมคอมพิวเตอร์",
                "credit": 3,
                "condition": ""
            }
        ]
        
        # Create temporary file
        temp_file = self.create_temp_json_file(course_data, "course_")
        
        try:
            # Call the import function
            import_course_from_json(temp_file)
            
            # Check course was created correctly and linked to 2560 curriculum
            self.assertEqual(Course.objects.count(), 1)
            course = Course.objects.first()
            self.assertEqual(course.course_id, "01418112-63")
            self.assertEqual(course.subcategory_fk, subcategory_2560)  # Should link to 2560 not 2565
        finally:
            # Clean up
            os.unlink(temp_file)
    
    def test_import_course_with_multiple_entries(self):
        """Test importing multiple courses from JSON file"""
        # Create test curriculum, category and subcategory first
        curriculum = Curriculum.objects.create(
            curriculum_name="Test Curriculum",
            total_credit=130,
            curriculum_year=2560
        )
        
        category = Category.objects.create(
            curriculum_fk=curriculum,
            category_name="หมวดวิชาเฉพาะ",
            category_min_credit=94
        )
        
        subcategory = Subcategory.objects.create(
            category_fk=category,
            subcategory_name="วิชาแกน",
            subcateory_min_credit=15
        )
        
        # Create test course data with multiple entries
        course_data = [
            {
                "str": 60,
                "field": "เฉพาะ",
                "tag": "แกน",
                "code": "01418112-60",
                "eng_name": "Computer Programming",
                "thai_name": "การเขียนโปรแกรมคอมพิวเตอร์",
                "credit": 3,
                "condition": ""
            },
            {
                "str": 60,
                "field": "เฉพาะ",
                "tag": "แกน",
                "code": "01418113-60",
                "eng_name": "Data Structures",
                "thai_name": "โครงสร้างข้อมูล",
                "credit": 3,
                "condition": "Prerequisite: 01418112-60"
            }
        ]
        
        # Create temporary file
        temp_file = self.create_temp_json_file(course_data, "course_")
        
        try:
            # Call the import function
            import_course_from_json(temp_file)
            
            # Check courses were created correctly
            self.assertEqual(Course.objects.count(), 2)
            course1 = Course.objects.get(course_id="01418112-60")
            course2 = Course.objects.get(course_id="01418113-60")
            self.assertEqual(course1.course_name_en, "Computer Programming")
            self.assertEqual(course2.course_name_en, "Data Structures")
        finally:
            # Clean up
            os.unlink(temp_file)