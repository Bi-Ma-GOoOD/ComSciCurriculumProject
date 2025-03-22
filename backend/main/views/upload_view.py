from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from minio import Minio
from minio.error import S3Error
from ..models import Form, User
from ..services import OCRService
from ..serializers import FileUploadSerializer
from django.conf import settings

class FileUploadView(APIView):
    def post(self, request):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
                files = [
                    request.FILES.get("transcript"),
                    request.FILES.get("activity"),
                    request.FILES.get("receipt")
                ]
                user_id = request.data.get("user_id")
                ocr_service = OCRService()
                validation_result = ocr_service.check_validation(files, user_id)
                if validation_result.get("status") == "success":
                    return Response(validation_result, status=HTTP_200_OK)
                else:
                    return Response(validation_result, status=HTTP_400_BAD_REQUEST)
                
                
            
            
            

            
            

