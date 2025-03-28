from typing import Dict, List
from rest_framework import serializers  # Adjust the import path as necessary

class StudyVerificationSerializer(serializers.Serializer):
    def to_representation(self, instance):
        if not (
            isinstance(instance.get('is_pass'), bool) and
            isinstance(instance.get('result'), List) and
            isinstance(instance.get('total_min_credit'), int) and
            isinstance(instance.get('acquired_credit'), int) and
            isinstance(instance.get('not_pass_course'), List)
            ) :
            raise Exception('expected object with attribute name "credit_detail", "subcategory_details" and "not_pass_course" in StudyVerificationSerializer class')
            
        return {
            'is_pass': instance.get('is_pass'),
            'total_min_credit': instance.get('total_min_credit'),
            'acquired_credit': instance.get('acquired_credit'),
            'result': self.getResults(instance.get('result')),
            'not_pass_course': self.getNotPassCourse(instance.get('not_pass_course'))
        }
        
    def getResults(self, obj) :
        return CourseResultSerializer(obj, many=True).data
    
    def getNotPassCourse(self, obj) :
        return NotPassCourseSerializer(obj, many=True).data
    
class CourseResultSerializer(serializers.Serializer) :
    def to_representation(self, instance):
        if not (
            isinstance(instance.get('category_name'), str) and
            isinstance(instance.get('is_pass'), bool) and
            isinstance(instance.get('acquired_credit'), int) and
            isinstance(instance.get('subcategories'), List) and
            isinstance(instance.get('total_min_credit'), int)
            ) :
            raise Exception('expected object with attribute name "category_name", "is_pass", "acquired", "subcategories" in CourseResultSerializer class')
        
        return {
            'category_name': instance.get('category_name'),
            'is_pass': instance.get('is_pass'),
            'acquired_credit': instance.get('acquired_credit'),
            'total_min_credit': instance.get('total_min_credit'),
            'subcategories': self.getSubcategories(instance.get('subcategories'))
        }
        
    def getSubcategories(self, obj) :
        return SubcateResultSerializer(obj, many=True).data
        
class SubcateResultSerializer(serializers.Serializer) :
    def to_representation(self, instance):        
        if not (
            isinstance(instance.get('subcategory_name'), str) and
            isinstance(instance.get('acquired_credit'), int) and
            isinstance(instance.get('is_pass'), bool) and
            isinstance(instance.get('total_min_credit'), int)
            ) :
            raise Exception('expected object with attribute name "subcategory_fk", "acquired_credit" and "is_pass" in SubcateResultSerializer class')
        
        return {
            'subcategory_name': instance.get('subcategory_name'),
            'acquired_credit': instance.get('acquired_credit'),
            'total_min_credit': instance.get('total_min_credit'),
            'is_pass': instance.get('is_pass'),
        }
        
class NotPassCourseSerializer(serializers.Serializer) :
    def to_representation(self, instance):
        if not (
            isinstance(instance.get('course_id'), str) and
            isinstance(instance.get('course_name_th'), str) and
            isinstance(instance.get('course_name_en'), str) and
            isinstance(instance.get('grade'), str)
            ) :
            raise Exception('expected object with attribute name "course_id" in NotPassCourseSerializer class')
        
        return {
            'course_id': instance.get('course_id'),
            'course_name_th': instance.get('course_name_th'),
            'course_name_en': instance.get('course_name_en'),
            'grade': instance.get('grade')
        }
        