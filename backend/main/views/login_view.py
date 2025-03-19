from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from main.services.login_service import LoginService

@csrf_exempt
@require_POST
def login_view(request):
    """
    Handle login requests from the frontend
    """
    try:
        # Parse JSON data from request body
        data = json.loads(request.body)
        email = data.get('email', '')
        password = data.get('password', '')
        
        # Authenticate user using LoginService
        success, result = LoginService.authenticate_user(email, password)
        
        if success:
            # User authenticated successfully
            user = result
            
            # Get user's form and determine redirect URL
            form = LoginService.get_user_form(user)
            redirect_url = LoginService.get_redirect_url(form)
            
            # Get user files if needed
            files = LoginService.get_user_files(form)
            
            # Create response with user information and redirect URL
            response_data = {
                'success': True,
                'message': 'Login successful',
                'user': {
                    'id': user.user_id,
                    'email': user.email,
                    'role': user.role,
                    'name': user.name,
                },
                'redirect_url': redirect_url,
            }
            
            return JsonResponse(response_data)
        else:
            # Authentication failed
            error_message = result
            return JsonResponse({
                'success': False,
                'message': error_message
            }, status=401)
            
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Server error: {str(e)}'
        }, status=500)