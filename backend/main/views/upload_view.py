from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from minio import Minio
from minio.error import S3Error
from ..models import Form, User
from ..services import OCRService
from ..serializers import FileUploadSerializer
from django.conf import settings

ocr_service = OCRService()

class FileUploadView(APIView):
    def get(self, request):
        user_id = request.query_params.get("user_id")
        response = ocr_service.get_form_view(user_id)
        if response.get("status") == "success":
            return Response(response, status=HTTP_200_OK)
        else:
            return Response(response, status=HTTP_400_BAD_REQUEST)
        
    def post(self, request):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
                files = [
                    request.FILES.get("transcript"),
                    request.FILES.get("activity"),
                    request.FILES.get("receipt")
                ]
                user_id = request.data.get("user_id")
                response = ocr_service.check_validation(files, user_id)
                print(response)
                if response.get("status") == "success":
                    return Response(response, status=HTTP_200_OK)
                else:
                    return Response(response, status=HTTP_400_BAD_REQUEST)
                
                
            
            
            

            
            

