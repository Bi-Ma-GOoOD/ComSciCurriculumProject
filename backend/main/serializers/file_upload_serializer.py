from rest_framework import serializers

class FileUploadSerializer(serializers.Serializer):
    transcript = serializers.FileField(required=False)
    activity = serializers.FileField(required=False)
    receipt = serializers.FileField(required=False)
    
    # form_id = serializers.UUIDField(required=True)
    # user_id = serializers.UUIDField(required=True) 
    
