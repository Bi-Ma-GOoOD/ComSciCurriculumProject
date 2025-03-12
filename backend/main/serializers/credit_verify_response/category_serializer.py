from typing import List
from rest_framework import serializers

from ...models import Category, Course
from .subcategory_serializer import SubcategorySerializer
from .course_serializer import CourseSerializer

class CategorySerializer(serializers.Serializer) :
    category_name = serializers.CharField()
    min_credit = serializers.IntegerField()
    subcategories = serializers.SerializerMethodField()
    courses = serializers.SerializerMethodField()
    is_complete = serializers.BooleanField()
    gpax = serializers.DecimalField(max_digits=3, decimal_places=2)
    
    def to_representation(self, instance):
        if not (
            instance.get('category') and
            isinstance(instance.get('courses_or_subcategories'), list) and
            isinstance(instance.get('isFreeElective'), bool) and
            isinstance(instance.get('isComplete'), bool) and
            isinstance(instance.get('totalWeightedGrade'), float) and
            isinstance(instance.get('totalCredit'), int)
        ) :
            raise serializers.ValidationError('expected object with attribute name "category" and "courses_or_subcategories" and "isFreeElective" and "isComplete" in CategorySerializer class')
        if not isinstance(instance['category'], Category) :
            raise serializers.ValidationError('unexpected object type in CategorySerializer class')

        if instance['isFreeElective'] :
            # incase of have no subcategory ex. หมวดวิชาเสรี
            return {
                'category_id': str(instance['category'].category_id),
                'category_name': instance['category'].category_name,
                'min_credit': instance['category'].category_min_credit,
                'is_complete': instance['isComplete'],
                'gpax': instance['totalWeightedGrade']/instance['totalCredit']  if instance['totalCredit'] != 0 else 0,
                'total_credit': instance['totalCredit'],
                'courses': self.get_courses(instance['courses_or_subcategories']),
            }
        
        return {
            'category_id': str(instance['category'].category_id),
            'category_name': instance['category'].category_name,
            'min_credit': instance['category'].category_min_credit,
            'is_complete': instance['isComplete'],
            'gpax': instance['totalWeightedGrade']/instance['totalCredit'] if instance['totalCredit'] != 0 else 0,
            'total_credit': instance['totalCredit'],
            'subcategories': self.get_subcategories(instance['courses_or_subcategories']),
        }
        
    def get_subcategories(self, obj) :
        return SubcategorySerializer(obj, many=True).data
    
    def get_courses(self, obj) :
        return CourseSerializer(obj, many=True).data