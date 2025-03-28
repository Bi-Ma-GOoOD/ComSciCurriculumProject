from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from ..services import OCRService
from ..serializers import FileUploadSerializer

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
        print(serializer)
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
                
        return Response({'message': 'some thing went wrong...'}, status=HTTP_400_BAD_REQUEST)
                
    def put(self, request):
        user_id = request.query_params.get("uid")
        form_type = request.query_params.get("form_type")
        response = ocr_service.change_form_type(user_id, form_type)
        if response.get("status") == "success":
            return Response(response, status=HTTP_200_OK)
        else:
            return Response(response, status=HTTP_400_BAD_REQUEST)
                
                
            
            
            




