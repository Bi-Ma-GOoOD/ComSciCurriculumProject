from rest_framework.response import Response
from main.services.view_pending_forms_service import ViewPendingFormsService
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def pending_forms_view(request):
    # Check if request method is GET
    if request.method != 'GET':
        return JsonResponse({
            'success': False,
            'message': 'Method not allowed'
        }, status=405)
    
    # Optional: Mock user for testing
    ViewPendingFormsService.mock_user_form()

    # Get pending forms data from service
    forms_data = ViewPendingFormsService.get_pending_forms()
        
    return JsonResponse({
        'success': True,
        'forms': forms_data
    })












