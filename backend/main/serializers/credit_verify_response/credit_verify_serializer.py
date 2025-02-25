from rest_framework import serializers

from .category_serializer import CategorySerializer
from .curriculum_serializer import CurriculumSerializer

class CreditVerifySerializer(serializers.Serializer) :
    curriculum = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()
    is_complete = serializers.BooleanField()
    gpax = serializers.DecimalField(max_digits=3, decimal_places=2)
    
    def to_representation(self, instance):
        if not (
            instance.get('curriculum') and
            instance.get('categories') and
            isinstance(instance.get('isComplete'), bool) and
            isinstance(instance.get('gpax'), float)
        ) :
            raise serializers.ValidationError('expect object with attribute name "curriculum" and "categories" and "isComplete" in CreditVerifySerializer class')
        
        return {
            'is_complete': instance['isComplete'],
            'gpax': instance['gpax'],
            'curriculum': self.get_curriculum(instance['curriculum']),
            'categories': self.get_categories(instance['categories']),
        }
        
    def get_curriculum(self, obj) :
        return CurriculumSerializer(obj).data

    def get_categories(self, obj) :
        return CategorySerializer(obj, many=True).data