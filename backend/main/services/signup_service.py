from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from main.models import OTPVerification, User, Form

class SignupService() :
    """
    Unified service class for handling authentication, OTP, user creation and form operations
    """
    
    @staticmethod
    def generate_and_save_otp(email):
        """Generate OTP, save it to database and return the OTP and reference"""
        otp = OTPVerification.generate_otp()
        reference = OTPVerification.generate_reference()
        
        # Save OTP verification record
        OTPVerification.objects.create(
            email=email,
            otp=otp,
            reference_otp=reference,
        )
        
        return otp, reference
    
    @staticmethod
    def send_otp_email(email, otp, reference):
        """Send OTP email to the user"""
        
        # Check if email is a KU email
        if email.endswith('@ku.th') and email.count('@') == 1:
            try:
                send_mail(
                    'Your Sign Up OTP',
                    f'Your One-Time Password #{reference} is: {otp}\nIt will expire in 10 minutes.',
                    'xxxxxxxxxxxx@gmail.com',  # SENDER EMAIL
                    [email],
                    fail_silently=False,
                )
                return True, None
            except Exception as e:
                return False, str(e)
        else:
            return False, "Only @ku.th email addresses are allowed for registration"
    
    @staticmethod
    def verify_otp(email, entered_otp, expiration_minutes=10):
        """Verify if OTP is valid and not expired"""
        # Check if OTP matches and is not expired
        otp_obj = OTPVerification.objects.filter(
            email=email,
            created_at__gte=timezone.now() - timedelta(minutes=expiration_minutes)
        ).last()
        
        if not otp_obj:
            return False, "OTP expired or not found"
            
        if len(entered_otp) != 6:
            return False, "OTP must be exactly 6 digits"
            
        if otp_obj.otp != entered_otp:
            return False, "Invalid OTP"
            
        return True, None
    
    @staticmethod
    def cleanup_otp(email):
        """Delete all OTP records for an email"""
        OTPVerification.objects.filter(email=email).delete()
    
    # User validation and creation methods
    @staticmethod
    def validate_registration_data(password, confirm_password, role, student_code, key_code):
        """Validate registration form data"""
        if password != confirm_password:
            return False, "Passwords do not match"
            
        if role == 'student' and not student_code:
            return False, "Student code is required for students"
            
        if role == 'student' and User.objects.filter(student_code=student_code).exists():
            return False, "Student code already exists"
            
        if role == 'inspector' and not key_code:
            return False, "Key code is required for inspectors"
            
        if role == 'inspector' and not SignupService.validate_key_code(key_code):
            return False, "Invalid key code"
            
        return True, None
    
    @staticmethod
    def validate_key_code(key_code):
        """Validate inspector key code"""
        valid_key_codes = ['INSPECTOR123']  # KEY CODES FOR INSPECTORS
        return key_code in valid_key_codes
    
    @staticmethod
    def create_user(email, password, name, role, student_code=None):
        """Create a new user based on role"""
        if role == 'student':
            user = User.objects.create(
                email=email,
                password=password,
                name=name,
                student_code=student_code,
                role=User.Role.STUDENT
            )
            
            # Create new form for student
            SignupService.create_graduation_check_form(user)
            
        elif role == 'inspector':
            user = User.objects.create(
                email=email,
                password=password,
                name=name,
                student_code=student_code,
                role=User.Role.INSPECTOR
            )
            
        return user
    
    # Form related methods
    @staticmethod
    def create_graduation_check_form(user):
        """Create a graduation check form for a student"""
        form = Form.objects.create(
            form_status=Form.FormStatus.DRAFT,
            form_type=Form.FormType.GRADUATION_CHECK,
            user_fk=user
        )
        return form