from rest_framework import serializers

from .not_pass_course_serializer import NotPassCourseSerializer
from .category_serializer import CategorySerializer
from .curriculum_serializer import CurriculumSerializer

class CreditVerifySerializer(serializers.Serializer) :
    curriculum = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()
    is_complete = serializers.BooleanField()
    gpax = serializers.DecimalField(max_digits=3, decimal_places=2)
    total_credit = serializers.IntegerField()
    
    def to_representation(self, instance):
        if not (
            instance.get('curriculum') and
            isinstance(instance.get('categories'), list) and
            isinstance(instance.get('isComplete'), bool) and
            isinstance(instance.get('gpax'), float) and
            isinstance(instance.get('credit'), int) and
            isinstance(instance.get('restudyRequire'), list)
        ) :
            raise serializers.ValidationError('expect object with attribute name "curriculum" and "categories" and "isComplete" in CreditVerifySerializer class')
        
        return {
            'is_complete': instance['isComplete'],
            'gpax': instance['gpax'],
            'total_credit': instance['credit'],
            'curriculum': self.get_curriculum(instance['curriculum']),
            'categories': self.get_categories(instance['categories']),
            'restudy_require': self.get_restudyRequire(instance['restudyRequire'])
        }
        
    def get_curriculum(self, obj) :
        return CurriculumSerializer(obj).data

    def get_categories(self, obj) :
        return CategorySerializer(obj, many=True).data
    
    def get_restudyRequire(self, obj) :
        return NotPassCourseSerializer(obj, many=True).data