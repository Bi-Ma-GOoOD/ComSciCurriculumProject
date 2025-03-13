from rest_framework import serializers

from ...models import Enrollment, CaluculatedEnrollment

class StudyResultSerializer(serializers.Serializer) :
    studied_semester = serializers.IntegerField()
    studied_year = serializers.IntegerField()
    grade = serializers.DecimalField(max_digits=3, decimal_places=2)
    
    def to_representation(self, instance):
        if not isinstance(instance, CaluculatedEnrollment) :
            raise serializers.ValidationError('unexpected object type in StudyResultSerializer class')

        return {
            'studied_semester': instance.enrollment.semester.value,
            'studied_year': instance.enrollment.year,
            'grade': instance.totalGrade if instance.totalGrade != None else instance.charGrade,
        }