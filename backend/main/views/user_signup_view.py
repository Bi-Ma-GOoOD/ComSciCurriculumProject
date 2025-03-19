from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

from main.services.signup_service import SignupService

@csrf_exempt
@require_http_methods(["POST"])
def user_signup_view(request):
    """
    Handle final user registration after OTP verification
    Creates user account based on role and provided details
    """
    try:
        # Parse incoming JSON data
        data = json.loads(request.body)
        
        # Extract required fields
        email = data.get('email', '').strip()
        password = data.get('password', '')
        confirm_password = data.get('confirmPassword', '')
        role_th = data.get('role', '')  # Role in Thai
        student_code = data.get('studentCode', '').strip()
        key_code = data.get('keyCode', '').strip()
        name = data.get('name', 'User')  # Default name if not provided
        
        # Map Thai role to English (for backend processing)
        role_map = {
            "นิสิต": "student",
            "ผู้ตรวจสอบหลักฐาน": "inspector"
        }
        role = role_map.get(role_th, "")
                
        # Validate required fields
        if not email:
            return JsonResponse({
                'success': False, 
                'message': 'Email is required'
            }, status=400)
            
        if not password or not confirm_password:
            return JsonResponse({
                'success': False, 
                'message': 'Password and password confirmation are required'
            }, status=400)
            
        if not role:
            return JsonResponse({
                'success': False, 
                'message': 'Role selection is required'
            }, status=400)
        
        # Validate registration data using the service
        is_valid, error_message = SignupService.validate_registration_data(
            password, confirm_password, role, student_code, key_code
        )
        
        if not is_valid:
            return JsonResponse({
                'success': False, 
                'message': error_message
            }, status=400)
        
        # Create user
        try:
            user = SignupService.create_user(
                email=email,
                password=password,
                name=name,
                role=role,
                student_code=student_code if role == 'student' else None
            )
            
            # Clean up OTP records after successful registration
            SignupService.cleanup_otp(email)
            
            # Return success response
            return JsonResponse({
                'success': True,
                'message': 'Registration successful',
                'userId': str(user.user_id),
                'role': role
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False, 
                'message': f'Failed to create user: {str(e)}'
            }, status=500)
    
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