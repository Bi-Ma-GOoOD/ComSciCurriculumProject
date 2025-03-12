from rest_framework import serializers

from ...models import Course
from .study_result_serializer import StudyResultSerializer

class CourseSerializer(serializers.Serializer) :
    course_id = serializers.CharField()
    course_name_th = serializers.CharField()
    course_name_en = serializers.CharField()
    credit = serializers.IntegerField()
    results = serializers.SerializerMethodField()
    
    def to_representation(self, instance):
        if not (instance.get('course') and instance.get('studyResult')) :
            raise serializers.ValidationError('expected object with attribute name "course" and "studyResult" in CourseSerializer class')
        if not isinstance(instance['course'], Course) :
            raise serializers.ValidationError('unexpected object type in CourseSerializer class')
            
        return {
            'course_id': instance['course'].course_id,
            'course_name_th': instance['course'].course_name_th,
            'course_name_en': instance['course'].course_name_en,
            'credit': instance['course'].credit,
            'results': self.get_results(instance['studyResult']),
        }
        
    def get_results(self, studyResultSerialized) :
        return StudyResultSerializer(studyResultSerialized).data
        
    