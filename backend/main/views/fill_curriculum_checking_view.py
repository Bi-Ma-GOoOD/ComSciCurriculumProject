from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from main.services.fill_curriculum_checking_service import FillCurriculumCheckingService

@csrf_exempt
@require_http_methods(["GET"])
def fillCurriculumCheckingView(request):
    service = FillCurriculumCheckingService()
    # FillCurriculumCheckingService.generate_and_upload(service, "8494c72a6a21456a8d0e446d93b51465")      # This is the user_id
    return JsonResponse({"message": "Form filled successfully!"})




# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.views.decorators.http import require_http_methods
# from django.core.exceptions import ObjectDoesNotExist
# import json
# import uuid

# from main.services.fill_curriculum_checking_service import FillCurriculumCheckingService
# from main.models import User

# @csrf_exempt
# @require_http_methods(["GET"])
# def fillCurriculumCheckingView(request):
#     """
#     View to generate and upload curriculum checking form for a student
    
#     Query Parameters:
#     - user_id: UUID of the student
#     - template_version (optional): Template version to use (default: 2565)
    
#     Returns:
#     - JSON response with download URLs and filenames
#     """
#     try:
#         # Get user_id from query parameters, defaulting to None if not provided
#         user_id = request.GET.get('user_id')
        
#         # Validate user_id is provided
#         if not user_id:
#             return JsonResponse({
#                 "status": "error", 
#                 "message": "User ID is required"
#             }, status=400)
        
#         # Validate user exists
#         try:
#             User.objects.get(user_id=user_id)
#         except ObjectDoesNotExist:
#             return JsonResponse({
#                 "status": "error", 
#                 "message": "User not found"
#             }, status=404)
        
#         # Get optional template version, default to 2565
#         template_version = request.GET.get('template_version', '2565')
        
#         # Initialize service
#         service = FillCurriculumCheckingService()
        
#         # Generate and upload PDF and QR code
#         pdf_url, pdf_filename, qr_url, qr_filename = service.generate_and_upload(
#             user_id, 
#             template_version
#         )
        
#         # Prepare response
#         response_data = {
#             "status": "success",
#             "pdf": {
#                 "url": pdf_url,
#                 "filename": pdf_filename
#             }
#         }
        
#         # Add QR code details if generated
#         if qr_url and qr_filename:
#             response_data["qr_code"] = {
#                 "url": qr_url,
#                 "filename": qr_filename
#             }
        
#         return JsonResponse(response_data)
    
#     except Exception as e:
#         # Catch any unexpected errors
#         return JsonResponse({
#             "status": "error", 
#             "message": str(e)
#         }, status=500)