# tests.py
from django.test import TestCase
from django.db import transaction
from main.models import Curriculum, Category, Subcategory
from pathlib import Path
import json

# Model Test
class CurriculumModelTest(TestCase):
    def setUp(self):
        # Create sample data for testing
        self.curriculum = Curriculum.objects.create(
            curriculum_name="หลักสูตรวิทยาศาสตรบัณฑิต สาขาวิชาวิทยาการคอมพิวเตอร์",
            total_credit=128,
            curriculum_year=2560
        )

        self.category = Category.objects.create(
            curriculum_fk=self.curriculum,
            category_name="หมวดวิชาศึกษาทั่วไป",
            category_min_credit=30
        )

        self.subcategory = Subcategory.objects.create(
            category_fk=self.category,
            subcategory_name="กลุ่มสาระอยู่ดีมีสุข",
            subcateory_min_credit=3
        )

    # test curriculum
    def test_curriculum_creation(self):
        """Test that a curriculum can be created with valid data"""
        self.assertEqual(self.curriculum.curriculum_name, "หลักสูตรวิทยาศาสตรบัณฑิต สาขาวิชาวิทยาการคอมพิวเตอร์")
        self.assertEqual(self.curriculum.total_credit, 128)
        self.assertEqual(self.curriculum.curriculum_year, 2560)

    def test_curriculum_str_method(self):
        """Test the string representation of Curriculum"""
        expected_str = f"curriculum name: {self.curriculum.curriculum_name}, {self.curriculum.curriculum_year}, {self.curriculum.total_credit}"
        self.assertEqual(str(self.curriculum), expected_str)

    # test category
    def test_category_creation(self):
        """Test that a category can be created and linked to curriculum"""
        self.assertEqual(self.category.category_name, "หมวดวิชาศึกษาทั่วไป")
        self.assertEqual(self.category.category_min_credit, 30)
        self.assertEqual(self.category.curriculum_fk, self.curriculum)

    def test_category_str_method(self):
        """Test the string representation of Category"""
        expected_str = f"course category: {self.category.category_name}"
        self.assertEqual(str(self.category), expected_str)

    # test subcategory
    def test_subcategory_creation(self):
        """Test that a subcategory can be created and linked to category"""
        self.assertEqual(self.subcategory.subcategory_name, "กลุ่มสาระอยู่ดีมีสุข")
        self.assertEqual(self.subcategory.subcateory_min_credit, 3)
        self.assertEqual(self.subcategory.category_fk, self.category)

    def test_subcategory_str_method(self):
        """Test the string representation of Subcategory"""
        expected_str = f"subcategory name {self.subcategory.subcategory_name}"
        self.assertEqual(str(self.subcategory), expected_str)

# Import Test
class CurriculumDataImportTest(TestCase):
    def test_multiple_json_data_import(self):
        """Test importing curriculum data from multiple JSON files"""
        # Get path to test data directory
        data_dir = Path(__file__).resolve().parent.parent / 'main' / 'data'
        json_files = ['curriculum_2560.json', 'curriculum_2565.json']
        
        total_expected_categories = 0
        total_expected_subcategories = 0
        
        # Process each JSON file
        for json_filename in json_files:
            json_file = data_dir / json_filename
            
            # Ensure test data file exists
            self.assertTrue(json_file.exists(), f"File {json_filename} not found")

            with open(json_file, "r", encoding="utf-8") as file:
                data = json.load(file)

            # Basic validation of JSON structure
            self.assertIn("curriculum", data)
            self.assertIn("course_structures", data)

            # Count expected number of categories and subcategories for this file
            for name in data.get("course_structures", []):
                for content in name.get("content", []):
                    if content.get("heading") == "โครงสร้างหลักสูตร :":
                        for structure in content.get("structure", []):
                            total_expected_categories += 1
                            total_expected_subcategories += len(structure.get("subsections", []))

        # After importing data, verify the total count of categories and subcategories
        self.assertEqual(Category.objects.count(), total_expected_categories)
        self.assertEqual(Subcategory.objects.count(), total_expected_subcategories)

    def test_individual_curriculum_data(self):
        """Test that each curriculum's data is correctly imported"""
        data_dir = Path(__file__).resolve().parent.parent / 'main' / 'data'
        json_files = ['curriculum_2560.json', 'curriculum_2565.json']
        
        for json_filename in json_files:
            json_file = data_dir / json_filename
            
            with open(json_file, "r", encoding="utf-8") as file:
                data = json.load(file)
                
            # Get curriculum info from the file
            curriculum_content = data.get("curriculum", {}).get("content", [])
            curriculum_name = ""
            curriculum_year = 0
            
            for content in curriculum_content:
                if content['heading'] == "รหัสและชื่อหลักสูตร":
                    curriculum_name = content['description'][1]
                elif content['heading'] == "สถานภาพของหลักสูตร":
                    curriculum_year = int(content['description'][0].split()[-1])
            
            # Verify this curriculum exists in database
            curriculum = Curriculum.objects.filter(
                curriculum_name=curriculum_name,
                curriculum_year=curriculum_year
            ).first()
            
            # verify this category exists in database
            categories = Category.objects.filter(
                curriculum_fk=curriculum
            )
            
            self.assertIsNotNone(curriculum, f"Curriculum from {json_filename} not found")
            
            # Count categories and subcategories for this specific curriculum
            expected_categories = 0
            expected_subcategories = 0
            
            for name in data.get("course_structures", []):
                for content in name.get("content", []):
                    if content.get("heading") == "โครงสร้างหลักสูตร :":
                        for structure in content.get("structure", []):
                            expected_categories += 1
                            expected_subcategories += len(structure.get("subsections", []))
            
            # Verify counts for this specific curriculum
            actual_categories = Category.objects.filter(
                curriculum_fk=curriculum
            ).count()
            
            actual_subcategories = 0
            
            for category in categories:
                actual_subcategories += Subcategory.objects.filter(
                    category_fk=category
                ).count()
            
            self.assertEqual(
                actual_categories, 
                expected_categories,
                f"Category count mismatch for {json_filename}"
            )
            self.assertEqual(
                actual_subcategories, 
                expected_subcategories,
                f"Subcategory count mismatch for {json_filename}"
            )