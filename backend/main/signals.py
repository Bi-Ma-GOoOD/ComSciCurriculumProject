from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.db import transaction
from django.conf import settings
from pathlib import Path
from .models import Curriculum, Category, Subcategory, Course
from django.db.models.functions import Cast
from django.db.models import Q, CharField, IntegerField
from django.db.models.functions import Cast, Substr, Length
import json
import re

def clean_title(text): 
    return re.sub(r'^\d+\.|\s*:$', '', text).strip()

def extract_number(text): 
    return int(re.search(r'\d+', text).group()) if re.search(r'\d+', text) else 0

def map_long_subtitle(text): 
    return "และเลือกเรียนรายวิชาใน 5 กลุ่มสาระ" if text.startswith("และเลือกเรียนรายวิชาใน 5 กลุ่มสาระ") else text

# Import curriculum data from JSON file
def import_curriculum_from_json(json_file_path):
    with open(json_file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
        curriculum_content = data.get("curriculum", {}).get("content", [])
        course_structures = data.get("course_structures", [])

    # Extract curriculum info
    curriculum_name = ""
    total_credits = 0
    curriculum_year = 0

    for content in curriculum_content:
        heading = content['heading']
        if heading == "รหัสและชื่อหลักสูตร":
            curriculum_name = content['description'][1]
        elif heading == "จำนวนหน่วยกิตที่เรียนตลอดหลักสูตร":
            total_credits = extract_number(content['headingDescription'])
        elif heading == "สถานภาพของหลักสูตร":
            curriculum_year = int(content['description'][0].split()[-1])

    # Create Curriculum
    curriculum = Curriculum.objects.create(
        curriculum_name=curriculum_name,
        total_credit=total_credits,
        curriculum_year=curriculum_year
    )

    # Process course structures
    for name in course_structures:
        for content in name['content']:
            if content['heading'] == "โครงสร้างหลักสูตร :":
                for structure in content['structure']:
                    category = Category.objects.create( # Create Category
                        curriculum_fk=curriculum,
                        category_name=clean_title(structure['title']),
                        category_min_credit=extract_number(structure['description'])
                    )
                    
                    for subsection in structure.get('subsections', []):
                        Subcategory.objects.create( # Create Subcategory
                            category_fk=category,
                            subcategory_name=map_long_subtitle(clean_title(subsection['subtitle'])),
                            subcateory_min_credit=extract_number(subsection['details'])
                        )
     
# Import course data from JSON file                        
def import_course_from_json(json_file_path):
    with open(json_file_path, "r", encoding="utf-8") as file:
        courses_data = json.load(file)

    for data in courses_data:
        course_code = data.get("code", "")
        course_eng_name = data.get("eng_name", "")
        course_thai_name = data.get("thai_name", "")
        course_credit = data.get("credit", 0)
        course_year = data.get("str")
        target_year = int(course_year)

        # Retrieve Curriculum based on str field        
        # Annotate with last two digits of curriculum_year for comparison
        curriculum = Curriculum.objects.annotate(
            year_str=Cast('curriculum_year', CharField()), # Converts the curriculum_year to a string
            last_two_digits=Cast(Substr('year_str', Length('year_str') - 1, 2), IntegerField()) # extracts 2 characters starting from position 3 and then converts this substring back to an integer
        ).filter(
            Q(year_str__endswith=str(course_year)) | # Find curriculum where the year string ends with the course_year
            Q(last_two_digits__lt=target_year) # Find curriculum where the last two digits are less than target_year
        ).order_by('-curriculum_year').first() # Sort results by curriculum_year in descending order
        
        if not curriculum:
            print(f"Curriculum '{data.get('str')}' not found for course '{course_code}'. Skipping.")
            continue
        
        # Retrieve Category based on field        
        category = Category.objects.filter(curriculum_fk=curriculum, category_name__contains=data.get("field")).first()
        
        if not category:
            print(f"Category '{data.get('field')}' not found for course '{course_code}'. Skipping.")
            continue
        
        # Retrieve Subcategory based on tag
        subcategory = Subcategory.objects.filter(category_fk=category, subcategory_name__contains=data.get("tag")).first()
        
        if not subcategory:
            print(f"Subcategory '{data.get('tag')}' not found for course '{course_code}'. Skipping.")
            continue

        # Create Course
        Course.objects.create(
            course_id=course_code,
            credit=course_credit,
            course_name_th=course_thai_name,
            course_name_en=course_eng_name,
            subcategory_fk=subcategory,
        )

@receiver(post_migrate)
def initialize_curriculum_data(sender, **kwargs):
    if sender.name == 'main':  # App name
        # Check if data already exists
        if Curriculum.objects.exists():
            return

        # Get the path to the data directory
        data_dir = Path(__file__).resolve().parent / 'data'
        
        # Process all JSON files in the data directory
        with transaction.atomic():
            # First, import all curriculum files
            for json_file in data_dir.glob('curriculum_*.json'):
                try:
                    import_curriculum_from_json(json_file)
                    print(f"Successfully imported curriculum data from {json_file.name}")
                except Exception as e:
                    print(f"Error importing {json_file.name}: {str(e)}")
            
            # Then, import all course files
            for json_file in data_dir.glob('*.json'):
                # Skip curriculum files as they're already processed
                if json_file.name.startswith('curriculum_'):
                    continue
                    
                try:
                    import_course_from_json(json_file)
                    print(f"Successfully imported course data from {json_file.name}")
                except Exception as e:
                    print(f"Error importing {json_file.name}: {str(e)}")