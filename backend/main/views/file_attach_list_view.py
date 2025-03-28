# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from django.conf import settings

# from main.models import Form
# from main.serializers import FormDetailSerializer
# from main.minio_client import generate_presigned_url

# class FileAttachListView(APIView):
#     def get(self, request):
#         form_id = request.query_params.get('form_id')
        
#         try:
#             form = Form.objects.get(form_id=form_id)
#             serializer = FormDetailSerializer(form)
            
#             # Predefined file types for graduation check
#             file_types = [
#                 'transcript',
#                 'activity',
#                 'receipt',
#                 # 'curriculum_check'
#             ]
            
#             # Generate presigned URLs for files
#             file_urls = {}
#             for file_type in file_types:
#                 # Construct file name based on student code and file type
#                 file_name = f"{form.form_id}/{file_type}.pdf"
                
#                 try:
#                     presigned_url = generate_presigned_url(file_name)
#                     file_urls[file_type] = presigned_url
#                 except Exception as e:
#                     file_urls[file_type] = None
#                     print(f"Error generating URL for {file_name}: {e}")
            
#             return Response({
#                 'form_details': serializer.data,
#                 'file_urls': file_urls
#             }, status=status.HTTP_200_OK)
        
#         except Form.DoesNotExist:
#             return Response({
#                 'error': 'Form not found'
#             }, status=status.HTTP_404_NOT_FOUND)
    
#     def post(self, request):
#         # Logic for file inspection and status update
#         form_id = request.data.get('form_id')
        
#         try:
#             form = Form.objects.get(form_id=form_id)
            
#             # Update form status to verified
#             form.form_status = Form.FormStatus.VERIFIED
#             form.save()
            
#             return Response({
#                 'message': 'Files verified successfully',
#                 'form_status': form.form_status
#             }, status=status.HTTP_200_OK)
        
#         except Form.DoesNotExist:
#             return Response({
#                 'error': 'Form not found'
#             }, status=status.HTTP_404_NOT_FOUND)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import FileResponse
from django.conf import settings

from main.models import Form
from main.serializers import FormDetailSerializer
from main.minio_client import generate_presigned_url, download_from_minio

class FileAttachListView(APIView):
    def get(self, request):
        form_id = request.query_params.get('form_id')
        file_type = request.query_params.get('file_type')
        download = request.query_params.get('download', 'false')
        
        try:
            form = Form.objects.get(form_id=form_id)
            
            # If download is requested
            if download.lower() == 'true' and file_type:
                # Construct file name based on form_id and file type
                file_name = f"{form_id}/{file_type}.pdf"
                
                # Download file from MinIO
                file_obj = download_from_minio(file_name)
                
                if file_obj:
                    # Create a file response
                    response = FileResponse(
                        file_obj.data, 
                        content_type='application/pdf',
                        as_attachment=True, 
                        filename=f"{form.user_fk.student_code}_{file_type}.pdf"
                    )
                    return response
                else:
                    return Response({
                        'error': 'File not found'
                    }, status=status.HTTP_404_NOT_FOUND)
            
            # Normal file details retrieval
            serializer = FormDetailSerializer(form)
            
            # Predefined file types for graduation check
            file_types = [
                'transcript',
                'activity',
                'receipt',
            ]
            
            # Generate presigned URLs for files
            file_urls = {}
            for file_type in file_types:
                # Construct file name based on form_id and file type
                file_name = f"{form_id}/{file_type}.pdf"
                
                try:
                    presigned_url = generate_presigned_url(file_name)
                    file_urls[file_type] = presigned_url
                except Exception as e:
                    file_urls[file_type] = None
                    print(f"Error generating URL for {file_name}: {e}")
            
            return Response({
                'form_details': serializer.data,
                'file_urls': file_urls
            }, status=status.HTTP_200_OK)
        
        except Form.DoesNotExist:
            return Response({
                'error': 'Form not found'
            }, status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request):
        # Logic for file inspection and status update
        form_id = request.data.get('form_id')
        
        try:
            form = Form.objects.get(form_id=form_id)
            
            # Update form status to verified
            form.form_status = Form.FormStatus.VERIFIED
            form.save()
            
            return Response({
                'message': 'Files verified successfully',
                'form_status': form.form_status
            }, status=status.HTTP_200_OK)
        
        except Form.DoesNotExist:
            return Response({
                'error': 'Form not found'
            }, status=status.HTTP_404_NOT_FOUND)