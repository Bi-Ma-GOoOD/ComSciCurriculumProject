from typing import List
from ..models import User, Curriculum, Category, Subcategory, Course, Enrollment, Form, VerificationResult

subjectNames = [
    {
        'name-th':'ศิลปะการอยู่ร่วมกับผู้อื่น',
        'name-en':'The Art of Living with Others',
        'code':'01387xx1-65',
    },
    {
        'name-th':'ปรัชญาเศรษฐกิจพอเพียงกับพุทธศาสนา',
        'name-en':'Philosophy of Sufficiency Economics and Buddhism',
        'code':'01387xx3-65',
    },
    {
        'name-th':'อาหารเพื่อมนุษยชาติ',
        'name-en':'Food for Mankind',
        'code':'01999xx1-65',
    },
    {
        'name-th':'เปตองเพื่อสุขภาพ',
        'name-en':'Petanque for Health',
        'code':'01175xx9-65',
    },
]

def mockUser() :
    user = User.objects.create(
        email='abc@gmail.com',
        password='1234',
        name='doe',
        student_code='6510450000',
        role=User.Role.STUDENT,
    )
    form = Form.objects.create(
        user_fk=user,
    )
    verification_result = VerificationResult.objects.create(
        form_fk=form,
    )

    return user, form, verification_result
    
def mockCurriculum() -> Curriculum :
    return Curriculum.objects.create(
        curriculum_name='หลักสูตรวิทยาศาสตรบัณฑิต สาขาวิชาวิทยาการคอมพิวเตอร์',
        total_credit=124,
        curriculum_year=2565,
    )
    
def mockCategories(curriculum: Curriculum) -> List[Category] :
    return [
        Category.objects.create(
            category_name='หมวดวิชาศึกษาทั่วไป',
            category_min_credit=4,
            curriculum_fk=curriculum,
        ),
        Category.objects.create(
            category_name='หมวดวิชาเสรี',
            category_min_credit=3,
            curriculum_fk=curriculum,
        ),   
    ]
    
def mockSubcategories(category: Category) -> List[Subcategory] :
    return [
        Subcategory.objects.create(
            subcategory_name='กลุ่มสาระอยู่ดีมีสุข',
            subcateory_min_credit=4,
            category_fk=category,
        )
    ]
    
def mockCourses(subcategory: Subcategory, credits: List[int]) -> List[Course] :
    
    return [
        Course.objects.create(
            course_id=subjectNames[i]['code'],
            credit=credits[i],
            course_name_th=subjectNames[i]['name-th'],
            course_name_en=subjectNames[i]['name-en'],
            subcategory_fk=subcategory,
        )
        for i in range(len(credits))
    ]
    
def mockEnrollments(user: User, course_and_grade_and_year: List[tuple[Course, float, int]]) :
    return [
        Enrollment.objects.create(
            semester=Enrollment.Semester.FIRST,
            year=year,
            user_fk=user,
            course_fk=course,
            grade=grade,
        )
        for course, grade, year in course_and_grade_and_year
    ]