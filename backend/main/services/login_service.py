from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from main.models import User, Form, VerificationResult, CreditDetail

class LoginService() :

    @staticmethod
    def authenticate_user(email, password):
        """
        Authenticate user with email and password
        """
        # Validate input
        if not email or not password:
            return False, "Email and password are required"
            
        # Check if email is a KU email
        if not email.endswith('@ku.th'):
            return False, "Only @ku.th email addresses are allowed"
        
        try:
            # Find user by email
            user = User.objects.get(email=email)
            
            # Check password
            if user.password == password: 
                return True, user
            else:
                return False, "Invalid email or password"
                
        except ObjectDoesNotExist:
            return False, "User not found"
        except Exception as e:
            return False, f"Login error: {str(e)}"
    
    @staticmethod
    def get_user_form(user):
        """
        Get user's form
        """
        try:
            form = Form.objects.filter(user_fk=user).first()
            return form
        except Exception:
            return None
    
    @staticmethod
    def check_exist_credit_detail(form):
        try:
            vr = VerificationResult.objects.get(form_fk=form)
            print(vr)
            if CreditDetail.objects.filter(verification_result_fk=vr).exists():
                return True
            else:
                return False
        except ObjectDoesNotExist:
            return False
        
    @staticmethod
    def get_redirect_url(form):
        """
        Redirect URL based on form type
        """
        if not form:
            return '/fileAttachCheck/'
        
        if LoginService.check_exist_credit_detail(form):
            return '/verify-result/'
        if form.form_type == Form.FormType.GRADUATION_CHECK:
            return '/insertGradFile/'
        elif form.form_type == Form.FormType.CREDIT_CHECK:
            return '/creditCheck/'
        else:
            return '/fileAttachCheck/'        # For INSPECTOR role
    
    @staticmethod
    def get_user_files(form):
        """
        Get files in user's form
        """
        if not form:
            return []
        else :
            # return File.objects.filter(form_id=form.form_id)
            return []  # until File model is implemented