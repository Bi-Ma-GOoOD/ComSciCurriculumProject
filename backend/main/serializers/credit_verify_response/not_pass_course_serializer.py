from rest_framework import serializers

from ...models import Enrollment

class NotPassCourseSerializer(serializers.ModelSerializer) :
    
    class Meta :
        model = Enrollment
        exclude = ['user_fk']