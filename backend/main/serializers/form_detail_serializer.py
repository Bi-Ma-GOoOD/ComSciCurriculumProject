from rest_framework import serializers
from main.models import Form, User

class FormDetailSerializer(serializers.ModelSerializer):
    student_code = serializers.CharField(source='user_fk.student_code', read_only=True)
    
    class Meta:
        model = Form
        fields = ['form_id', 'student_code', 'form_status', 'form_type']