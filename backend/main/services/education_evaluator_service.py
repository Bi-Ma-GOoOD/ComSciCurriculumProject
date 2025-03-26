import uuid

from ..models import Curriculum, Enrollment, Category, Subcategory, VerificationResult, CreditDetail, SubcategoryDetails, NotPassCourse, Form, User
from ..serializers import CreditVerifySerializer
from .calculator_service import CalculatorService
from ..utils import utils

class EducationEvaluationService() :
    def __init__(self):
        self.caculator = CalculatorService()
        
    def getCurriculumData(self, curriculum: Curriculum, mappingResult, freeElectiveDetail, nonElectiveCategoryDetail, subCategoryDetail) :
        # TODO freeElectiveDetail use only test before query
        # TODO nonElectiveCategoryDetail use only test before query (1. query category)
        # TODO subCategoryDetail use only test before query (2. query subcategory)
        
        restudyRequire = []
        
        isComplete = True
        categories = []
        totalWeightedGrade = 0
        totalCredit = 0
        
        # no elective category course
        for category in nonElectiveCategoryDetail :
            checked = self.getCategorizeCategoryDetail(
                categorizeCourses=mappingResult['categorize course'],
                categoryDetail=category,
                subcategoriesDetail=subCategoryDetail.get(category.category_name),
                restudyRequire=restudyRequire,
            )
            isComplete &= checked['isComplete']
            totalWeightedGrade += checked['totalWeightedGrade']
            totalCredit += checked['totalCredit']
            categories.append(checked)
            
        # elective category course
        freeElectiveCheck = self.getFreeElectionCategoryDetal(
            freeElectiveDetail=freeElectiveDetail, 
            freeElectiveEnrollment=mappingResult['free elective'],
            restudyRequire=restudyRequire,
        )
        isComplete &= freeElectiveCheck['isComplete']
        totalWeightedGrade += freeElectiveCheck['totalWeightedGrade']
        totalCredit += freeElectiveCheck['totalCredit']
        categories.append(freeElectiveCheck)
        
        gpax = totalWeightedGrade/float(totalCredit) if totalCredit != 0 else 0
        
        return {
            'curriculum': curriculum,
            'isComplete': isComplete and (gpax >= 2.00),
            'categories': categories,
            'gpax': gpax,
            'credit': totalCredit,
            'restudyRequire': restudyRequire,
        }
        
    def getFreeElectionCategoryDetal(self, freeElectiveEnrollment, freeElectiveDetail, restudyRequire) :
        studied = []
        totalCredit = 0
        totalWeightedGrade = 0
        
        for enrollment in freeElectiveEnrollment :
            credit = enrollment.enrollment.course_fk.credit
            grade = enrollment.totalGrade
            
            if grade != None :
                # no need to calculate further if result grade is F, N, I
                totalWeightedGrade += grade * credit
                
                totalCredit += credit
                
            if grade == None or grade == 0.0 :
                restudyRequire.append(enrollment.enrollment)
            
            studied.append({
                'course': enrollment.enrollment.course_fk,
                'studyResult': enrollment,
            })
        
        return {
            'category': freeElectiveDetail,
            'isComplete': totalWeightedGrade > 0 and (totalCredit >= freeElectiveDetail.category_min_credit),
            'totalCredit': totalCredit,
            'totalWeightedGrade': totalWeightedGrade if totalWeightedGrade != 0 else 0.0,
            'isFreeElective': True,
            'courses_or_subcategories': studied,
        }
        
    def getCategorizeCategoryDetail(self, categorizeCourses, categoryDetail, subcategoriesDetail, restudyRequire) :
        categorizeCoursesReformat = {}
        for categorizeCourse in categorizeCourses :
            categorizeCoursesReformat[categorizeCourse['subcategory'].subcategory_name] = list(categorizeCourse['matchEnrollment'].values())
            
        isComplete = True
        subcategories = []
        totalWeightedGrade = 0
        totalCredit = 0
        
        for subcategory in subcategoriesDetail :            
            checked = self.getSubcategoryDetail(subcategory, categorizeCoursesReformat, restudyRequire)
            
            if checked :
                subcategories.append(checked)
                isComplete &= checked['isComplete'] and (checked['totalWeightedGrade'] > 0)
                totalCredit += checked['totalCredit']
                totalWeightedGrade += checked['totalWeightedGrade']
        
        return {
            'category': categoryDetail,
            'isComplete': isComplete,
            'totalCredit': totalCredit,
            'totalWeightedGrade': totalWeightedGrade if totalWeightedGrade != 0 else 0.0,
            'isFreeElective': False,
            'courses_or_subcategories': subcategories,
        }
        
    def getSubcategoryDetail(self, subcategory, categorizeCourses, restudyRequire) :
        if not categorizeCourses.get(subcategory.subcategory_name) :
            return {
                'subcategory': subcategory,
                'isComplete': False,
                'courses': [],
                'totalWeightedGrade': 0.0,
                'totalCredit': 0,
            }
        
        studied = []
        totalWeightedGrade = 0
        totalCredit = 0
        
        for enrollment in categorizeCourses[subcategory.subcategory_name] :
            enrollment_subcategory = enrollment.enrollment.course_fk.subcategory_fk.subcategory_name
                
            if (
                enrollment_subcategory != subcategory.subcategory_name and
                enrollment_subcategory not in utils.UNIVERSITY_SUBCATEGORY
                ) :
                raise RuntimeError('Studied course doesn\'n match with subcategory in curriculum\'s subcategory.')
            
            credit = enrollment.enrollment.course_fk.credit
            grade = enrollment.totalGrade
            charGrade = enrollment.charGrade
            
            if isinstance(grade, float) :
                # no need to calculate further if result grade is F, N, I
                totalWeightedGrade += grade * credit
                
                totalCredit += credit
                
            if (grade == None and charGrade != 'P') or grade == 0.0 :
                restudyRequire.append(enrollment.enrollment)
            
            studied.append({
                'course': enrollment.enrollment.course_fk,
                'studyResult': enrollment,
            })
        
        return {
            'subcategory': subcategory,
            'isComplete': totalWeightedGrade > 0 and totalCredit >= subcategory.subcateory_min_credit,
            'courses': studied,
            'totalWeightedGrade': totalWeightedGrade if totalWeightedGrade != 0 else 0.0,
            'totalCredit': totalCredit,
        }
    
    def verify(self, userId :str, *args, **param) :    
        
        user = User.objects.get(user_id=userId)
        curriculum_year = int(user.student_code[:2]) - (int(user.student_code[:2]) % 5)
        curriculum = Curriculum.objects.get(curriculum_year=2500+curriculum_year)
        
        form = Form.objects.get(user_fk=userId)
        enrollments = []
        
        for enrollment in Enrollment.objects.filter(user_fk=userId) :
            enrollment.semester = Enrollment.Semester(enrollment.semester)
            enrollments.append(enrollment)
        
        verificationResult = VerificationResult.objects.get(form_fk=form.form_id)
        
        subcategoriesReformate = {}
        
        allCategory = Category.objects.all()
        allSubcategories = Subcategory.objects.all()
        
        if param.get('isTesting') and len(args) == 3 :
            categories, subcategories, courses = args
            
            categories = [[categories[0]], categories[1]]
        
            for subcategory in subcategories :
                categoryId = subcategory.category_fk.category_name
                if subcategoriesReformate.get(categoryId) :
                    subcategoriesReformate[categoryId].append(subcategory)
                else :
                    subcategoriesReformate[categoryId] = [subcategory] 
        
        else :
            subcategories = []
            
            categories = allCategory.filter(curriculum_fk=curriculum.curriculum_id)
            
            for category in categories :
                if category.category_name == 'หมวดวิชาเลือกเสรี' :
                    continue
                
                s = allSubcategories.filter(category_fk=category.category_id)
                subcategories.extend(e for e in s)
                
                subcategoriesReformate[category.category_name] = [e for e in s]
                
            categories = [[e for e in categories.exclude(category_name='หมวดวิชาเลือกเสรี')], categories.get(category_name='หมวดวิชาเลือกเสรี')]              
  
        cleanEnrollment = self.caculator.GPACalculate(enrollments)
        mappingResult = self.caculator.map(subcategories, cleanEnrollment)

        studyResult = CreditVerifySerializer(self.getCurriculumData(
            curriculum=curriculum,
            mappingResult=mappingResult,
            freeElectiveDetail = categories[1],
            nonElectiveCategoryDetail = categories[0],
            subCategoryDetail = subcategoriesReformate,
        )).data        
        
            
            
        try :
            form.form_status = Form.FormStatus.PENDING
            form.save()
            
            credit_detail = CreditDetail.objects.create(
                credit_status = CreditDetail.CreditStatus(1 if studyResult['is_complete'] else 0),
                verification_result_fk = verificationResult,
            )     
            
            for category in studyResult['categories'] :
                if category.get('subcategories') :
                    for subcategory in category['subcategories'] :
                        SubcategoryDetails.objects.create(
                            acquired_credit = subcategory['total_credit'],
                            is_pass = subcategory['is_complete'],
                            subcateory_fk = allSubcategories.get(subcategory_id=subcategory['subcategory_id']),
                            category_fk = allCategory.get(category_id=category['category_id']),
                            credit_detail_fk = credit_detail,
                        )
                        
                else :                    
                    SubcategoryDetails.objects.create(
                        acquired_credit = category['total_credit'],
                        is_pass = subcategory['is_complete'],
                        subcateory_fk = None,
                        category_fk = allCategory.get(category_id=category['category_id']),
                        credit_detail_fk = credit_detail,
                    )
                    
            for course in studyResult['restudy_require'] :
                NotPassCourse.objects.create(
                    credit_detail_fk = credit_detail,
                    enrollment_fk = Enrollment.objects.get(enrollment_id=course['enrollment_id']),
                )                  
        
        except Exception as e :
            print('Exception occurred:', e)
        finally :
            return studyResult