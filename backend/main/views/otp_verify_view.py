from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

from main.services.signup_service import SignupService

@csrf_exempt
@require_http_methods(["POST"])
def otp_verify_view(request):
    """
    Handle OTP verification during signup process
    Validates OTP and prepares for next signup step
    """
    try:
        # Parse incoming JSON data
        data = json.loads(request.body)
        email = data.get('email', '').strip()
        otp = data.get('otp', '').strip()
        reference = data.get('reference', '').strip()
        
        # Validate required fields
        if not email:
            return JsonResponse({
                'success': False, 
                'message': 'Email is required'
            }, status=400)
            
        if not otp:
            return JsonResponse({
                'success': False, 
                'message': 'OTP is required'
            }, status=400)
        
        # Verify OTP using the service
        verified, error_message = SignupService.verify_otp(email, otp, reference)
        
        if not verified:
            return JsonResponse({
                'success': False, 
                'message': error_message
            }, status=400)
        
        # OTP is valid - return success response
        return JsonResponse({
            'success': True,
            'message': 'OTP verified successfully',
            'email': email  # Return email for next step
        })
    
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False, 
            'message': 'Invalid JSON'
        }, status=400)
    
    except Exception as e:
        return JsonResponse({
            'success': False, 
            'message': str(e)
        }, status=500)