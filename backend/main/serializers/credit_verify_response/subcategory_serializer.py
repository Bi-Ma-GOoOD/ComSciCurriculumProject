from rest_framework import serializers

from ...models import Subcategory
from .course_serializer import CourseSerializer

class SubcategorySerializer(serializers.Serializer) :
    subcategory_name = serializers.CharField()
    min_credit = serializers.IntegerField()
    courses = serializers.SerializerMethodField()
    total_weighted_grade = serializers.DecimalField(max_digits=3, decimal_places=2)
    is_complete = serializers.BooleanField()
    
    def to_representation(self, instance):
        if not (
            instance.get('subcategory') and
            isinstance(instance.get('courses'), list) and
            isinstance(instance.get('isComplete'), bool) and
            isinstance(instance.get('totalWeightedGrade'), float) and
            isinstance(instance.get('totalCredit'), int)
        ) :
            raise serializers.ValidationError('expected object with attribute name "subcategory" and "courses" and "isComplete" in SubcategorySerializer class')
        if not isinstance(instance['subcategory'], Subcategory) :
            raise serializers.ValidationError('unexpected object type in SubcategorySerializer class')
        
        return {
            'subcategory_id': str(instance['subcategory'].subcategory_id),
            'subcategory_name': instance['subcategory'].subcategory_name,
            'min_credit': instance['subcategory'].subcateory_min_credit,
            'is_complete': instance['isComplete'],
            'gpax': instance['totalWeightedGrade']/instance['totalCredit'] if instance['totalCredit'] != 0 else 0,
            'total_credit': instance['totalCredit'],
            'courses': self.get_courses(instance['courses']),
        }
        
    def get_courses(self, obj) :
        return CourseSerializer(obj, many=True).data