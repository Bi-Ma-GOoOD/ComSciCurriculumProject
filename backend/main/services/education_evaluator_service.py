from typing import List

from ..models import Curriculum, Enrollment, Category, Subcategory
from ..serializers import CreditVerifySerializer
from .calculator_service import CalculatorService


class EducationEvaluationService() :
    def __init__(self):
        self.caculator = CalculatorService()
        
    def getCurriculumData(self, curriculum: Curriculum, mappingResult, **param) :
        # TODO freeElectiveDetail use only test before query
        # TODO nonElectiveCategoryDetail use only test before query (1. query category)
        # TODO subCategoryDetail use only test before query (2. query subcategory)
        if not (param and param.get('freeElectiveDetail')) : return
        if not (param and param.get('nonElectiveCategoryDetail')) : return # want [ categories, ... ]
        if not (param and param.get('subCategoryDetail')) : return # want { category: [subcategories, ...] }
        
        restudyRequire = []
        
        isComplete = True
        categories = []
        totalWeightedGrade = 0
        totalCredit = 0
        
        subcategoryDetailParam = dict(param.get('subCategoryDetail'))
        # no elective category course
        for category in param.get('nonElectiveCategoryDetail') :
            checked = self.getCategorizeCategoryDetail(
                categorizeCourses=mappingResult['categorize course'],
                categoryDetail=category,
                subcategoriesDetail=subcategoryDetailParam.get(category.category_name),
                restudyRequire=restudyRequire,
            )
            isComplete &= checked['isComplete']
            totalWeightedGrade += checked['totalWeightedGrade']
            totalCredit += checked['totalCredit']
            categories.append(checked)
            
        # elective category course
        freeElectiveCheck = self.getFreeElectionCategoryDetal(
            freeElectiveDetail=param.get('freeElectiveDetail'), 
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
                restudyRequire.append({
                    'course': enrollment.enrollment.course_fk,
                    'studyResult': enrollment,
                })
            
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
            return []
        
        studied = []
        totalWeightedGrade = 0
        totalCredit = 0
        
        for enrollment in categorizeCourses[subcategory.subcategory_name] :
            if enrollment.enrollment.course_fk.subcategory_fk.subcategory_id != subcategory.subcategory_id :
                raise RuntimeError('Studied course doesn\'n match with subcategory in curriculum\'s subcategory.')
            
            credit = enrollment.enrollment.course_fk.credit
            grade = enrollment.totalGrade
            
            if grade != None :
                # no need to calculate further if result grade is F, N, I
                totalWeightedGrade += grade * credit
                
                totalCredit += credit
                
            if grade == None or grade == 0.0 :
                restudyRequire.append({
                    'course': enrollment.enrollment.course_fk,
                    'studyResult': enrollment,
                })
            
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
    
    def verify(self, curriculum: Curriculum, enrollments: List[Enrollment], *args, **param) :
        subcategoriesReformate = {}
        
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
            
            categories = Category.objects.filter(curriculum_fk=curriculum.curriculum_id)
            
            allSubcategories = Subcategory.objects.all()
            for category in categories :
                if category.category_name == 'หมวดวิชาเลือกเสรี' :
                    continue
                
                subcategories.extend(e for e in allSubcategories.filter(category_fk=category.category_id))
                
                subcategoriesReformate[category.category_name] = [e for e in subcategories]
                
            categories = [[e for e in categories.exclude(category_name='หมวดวิชาเลือกเสรี')], categories.get(category_name='หมวดวิชาเลือกเสรี')]              
  
        cleanEnrollment = self.caculator.GPACalculate(enrollments)        
        mappingResult = self.caculator.map(subcategories, cleanEnrollment)

        studyResult = self.getCurriculumData(
            curriculum=curriculum,
            mappingResult=mappingResult,
            freeElectiveDetail = categories[1],
            nonElectiveCategoryDetail = categories[0],
            subCategoryDetail = subcategoriesReformate,
        )
        
        return CreditVerifySerializer(studyResult)