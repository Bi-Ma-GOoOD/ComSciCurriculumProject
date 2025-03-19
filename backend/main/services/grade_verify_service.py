from typing import List
import uuid

from ..models import Form, VerificationResult, CreditDetail, SubcategoryDetails, NotPassCourse
from ..serializers import StudyVerificationSerializer, OverallVerificationSerializer

class GradeVerificationService() :
    def __init__(self):
        pass
    
    def getVerification(self, uid: uuid.UUID) :
        # get form
        form = Form.objects.get(user_fk=uuid.UUID(uid))
        
        # get verification result
        vr = VerificationResult.objects.get(form_fk=form.form_id)
        
        # get credit detail
        cd = CreditDetail.objects.get(verification_result_fk=vr.verification_result_id)
        
        # get subcategory details
        sd = SubcategoryDetails.objects.filter(credit_detail_fk=cd.credit_details_id)
        
        # get not pass course
        not_pass_course = NotPassCourse.objects.filter(credit_detail_fk=cd.credit_details_id)
        
        studyResult = self.getDataSerializer(cd, sd, not_pass_course)
        feeResult = vr.fee_status
        activityResult = vr.activity_status
        
        if form.form_type == 'credit check' :
            return OverallVerificationSerializer({
                'studyResult': studyResult,
                'feeResult': feeResult,
                'activityResult': activityResult
            }).data
        else :
            return StudyVerificationSerializer(
                studyResult
            ).data
                
        
    def getDataSerializer(self, creditDetail: CreditDetail, subcategoryDetails: List[SubcategoryDetails], not_pass_course: List[NotPassCourse]) :
        cleanData = {}
        for subcategoryDetail in subcategoryDetails :
            categoryName = subcategoryDetail.category_fk.category_name
            if cleanData.get(categoryName) :
                cleanData[categoryName].append(subcategoryDetail)
            else :
                cleanData[categoryName] = [subcategoryDetail]
        
        return {
            'is_pass': bool(creditDetail.credit_status),
            'result': [self.getResult(e) for e in cleanData.values()],
            'not_pass_course': [self.getNotPassCourse(e) for e in not_pass_course]
        }
        
    def getResult(self, subcategoryDetails: List[SubcategoryDetails]) :
        isPass = True
        acquire = 0
        subcategories = []
        for subcategory in subcategoryDetails :
            subcate = self.getSubcate(subcategory)
            if subcate :
                isPass &= subcate.get('is_pass')
                acquire += subcate.get('acquired_credit')
                subcategories.append(subcate)
        
        return {
            'category_name': subcategoryDetails[0].category_fk.category_name,
            'is_pass': isPass,
            'acquired_credit': acquire,
            'subcategories': subcategories,
        } 
        
    def getSubcate(self, subcateDetail: SubcategoryDetails) :
        if not subcateDetail.subcateory_fk :
            return 
        return {
            'subcategory_name': subcateDetail.subcateory_fk.subcategory_name,
            'acquired_credit': subcateDetail.acquired_credit,
            'is_pass': subcateDetail.is_pass
        }
        
    def getNotPassCourse(self, notPassCourses: NotPassCourse) :
        return {
            'course_id': notPassCourses.enrollment_fk.course_fk.course_id,
            'course_name_th': notPassCourses.enrollment_fk.course_fk.course_name_th,
            'course_name_en': notPassCourses.enrollment_fk.course_fk.course_name_en,
            'grade': notPassCourses.enrollment_fk.grade,
        }
