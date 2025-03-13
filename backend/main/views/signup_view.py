from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

from main.services.signup_service import SignupService

@csrf_exempt
@require_http_methods(["POST"])
def signup_view(request):
    """
    Handle user signup initial registration step
    Validates email and prepares OTP
    """
    try:
        # Parse incoming JSON data
        data = json.loads(request.body)
        print("Received signup request:", data)
        email = data.get('email', '').strip()
        
        # Validate email is not empty
        if not email:
            return JsonResponse({
                'success': False, 
                'message': 'Email is required'
            }, status=400)
        
        # Validate email domain
        if not email.endswith('@ku.th'):
            return JsonResponse({
                'success': False, 
                'message': 'Only @ku.th email addresses are allowed'
            }, status=400)
        
        # Check if user already exists
        from main.models import User
        if User.objects.filter(email=email).exists():
            return JsonResponse({
                'success': False, 
                'message': 'Email already registered'
            }, status=400)
        
        # Generate OTP
        otp, reference = SignupService.generate_and_save_otp(email)
        
        # Send OTP email
        email_sent, error = SignupService.send_otp_email(email, otp, reference)
        
        if not email_sent:
            return JsonResponse({
                'success': False, 
                'message': error or 'Failed to send OTP email'
            }, status=500)
        
        # Return success response with reference for OTP verification
        return JsonResponse({
            'success': True, 
            'reference': reference,
            'message': 'OTP sent successfully'
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