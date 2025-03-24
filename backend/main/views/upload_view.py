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
            # try :
                # form = Form.objects.get(form_id=serializer.data.get("form_id"))
                files = [
                    request.FILES.get("transcript"),
                    request.FILES.get("activity"),
                    request.FILES.get("receipt")
                ]
                user_id = request.data.get("user_id")  # Retrieve user_id from the request
            # form.form_type
            # if not all(files):
            #     return Response({"message": "Files are missing.", "files": [f.name if f else None for f in files]}, status=HTTP_400_BAD_REQUEST)
            # else:
                ocr_service = OCRService()
                validation_result = ocr_service.check_validation(files)
                if validation_result.get("status") == "success":
                    return Response(validation_result, status=HTTP_200_OK)
                else:
                    return Response(validation_result, status=HTTP_400_BAD_REQUEST)
            # except Form.DoesNotExist:
            #     return Response({"message": "Form not found."}, status=HTTP_400_BAD_REQUEST)









