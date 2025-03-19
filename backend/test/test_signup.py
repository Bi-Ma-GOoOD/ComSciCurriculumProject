from django.test import TestCase
from unittest.mock import patch
from main.models import OTPVerification, User, Form
from main.services import SignupService  

class SignupServiceTest(TestCase):
    def setUp(self):
        OTPVerification.objects.all().delete()  # Clear any old OTP records
        self.email = "test@ku.th"
        self.student_code = "STU123"
        self.inspector_key = "INSPECTOR123"
        self.user = User.objects.create(email=self.email, role="student", student_code=self.student_code)
    
    def test_generate_and_save_otp(self):
        """Test OTP generation and saving to database"""
        email = "test@ku.th"
        otp, reference = SignupService.generate_and_save_otp(email)
        
        # Check that OTP is saved in the database
        self.assertTrue(OTPVerification.objects.filter(email=email, otp=otp, reference_otp=reference).exists())

    def test_send_otp_email(self):
        """Test OTP email sending"""
        email = "test@ku.th"
        otp, reference = "123456", "ABC123"
        success, error = SignupService.send_otp_email(email, otp, reference)
        
        self.assertTrue(success)
        self.assertIsNone(error)

    def test_verify_otp(self):
        """Test OTP verification"""
        email = "test@ku.th"
        otp, reference = SignupService.generate_and_save_otp(email)
        
        # Verify the OTP
        result, error = SignupService.verify_otp(email, otp)
        self.assertTrue(result)
        self.assertIsNone(error)

    def test_create_user(self):
        """Test user creation"""
        user = SignupService.create_user(
            email="student@ku.th",
            password="securepassword",
            name="John Doe",
            role=User.Role.STUDENT,
            student_code="ST12345"
        )
        
        self.assertEqual(user.email, "student@ku.th")
        self.assertEqual(user.role, User.Role.STUDENT)
        
        # Check if graduation form is created
        self.assertTrue(Form.objects.filter(user_fk=user, form_type=Form.FormType.GRADUATION_CHECK).exists())
        
    def test_cleanup_otp(self):
        """Test if cleanup_otp deletes all OTP records for a given email"""
        OTPVerification.objects.create(email=self.email, otp="123456", reference_otp="REF001")
        OTPVerification.objects.create(email=self.email, otp="654321", reference_otp="REF002")

        self.assertEqual(OTPVerification.objects.filter(email=self.email).count(), 2)
        
        SignupService.cleanup_otp(self.email)
        
        self.assertEqual(OTPVerification.objects.filter(email=self.email).count(), 0)


    def test_validate_registration_password_mismatch(self):
        """Test registration validation when passwords do not match"""
        is_valid, error = SignupService.validate_registration_data(
            "password123", "password456", "student", "STU123", None
        )
        self.assertFalse(is_valid)
        self.assertEqual(error, "Passwords do not match")

    def test_validate_registration_student_without_code(self):
        """Test registration validation when student code is missing"""
        is_valid, error = SignupService.validate_registration_data(
            "password123", "password123", "student", None, None
        )
        self.assertFalse(is_valid)
        self.assertEqual(error, "Student code is required for students")

    def test_validate_registration_student_code_already_exists(self):
        """Test registration validation when student code is already in use"""
        User.objects.create(email="another@ku.th", role="student", student_code="STU123")

        is_valid, error = SignupService.validate_registration_data(
            "password123", "password123", "student", "STU123", None
        )
        self.assertFalse(is_valid)
        self.assertEqual(error, "Student code already exists")

    def test_validate_registration_inspector_without_key_code(self):
        """Test registration validation when inspector key code is missing"""
        is_valid, error = SignupService.validate_registration_data(
            "password123", "password123", "inspector", None, None
        )
        self.assertFalse(is_valid)
        self.assertEqual(error, "Key code is required for inspectors")

    @patch("main.services.signup_service.SignupService.validate_key_code")
    def test_validate_registration_invalid_key_code(self, mock_validate_key_code):
        """Test registration validation when inspector key code is invalid"""
        mock_validate_key_code.return_value = False

        is_valid, error = SignupService.validate_registration_data(
            "password123", "password123", "inspector", None, "INVALID"
        )
        self.assertFalse(is_valid)
        self.assertEqual(error, "Invalid key code")

    def test_validate_registration_valid_student(self):
        """Test valid student registration"""
        is_valid, error = SignupService.validate_registration_data(
            "password123", "password123", "student", "NEWSTU123", None
        )
        self.assertTrue(is_valid)
        self.assertIsNone(error)

    def test_validate_registration_valid_inspector(self):
        """Test valid inspector registration"""
        is_valid, error = SignupService.validate_registration_data(
            "password123", "password123", "inspector", None, "INSPECTOR123"
        )
        self.assertTrue(is_valid)
        self.assertIsNone(error)

    def test_validate_key_code_valid(self):
        """Test valid inspector key code"""
        self.assertTrue(SignupService.validate_key_code("INSPECTOR123"))

    def test_validate_key_code_invalid(self):
        """Test invalid inspector key code"""
        self.assertFalse(SignupService.validate_key_code("INVALID"))

    def test_create_graduation_check_form(self):
        """Test if a graduation check form is created for a student"""
        form = SignupService.create_graduation_check_form(self.user)
        self.assertIsNotNone(form)
        self.assertEqual(form.user_fk, self.user)
        self.assertEqual(form.form_status, Form.FormStatus.DRAFT)
        self.assertEqual(form.form_type, Form.FormType.GRADUATION_CHECK)

    def test_send_otp_email_valid_ku_email(self):
        """Test sending OTP with a valid @ku.th email"""
        email = "student@ku.th"
        otp, reference = "123456", "ABC123"
        success, error = SignupService.send_otp_email(email, otp, reference)
        
        self.assertTrue(success)
        self.assertIsNone(error)

    def test_send_otp_email_invalid_email_domain(self):
        """Test sending OTP with an invalid email domain"""
        invalid_emails = [
            "student@gmail.com",
            "student@eng.ku.th",
            "student@something.ku.th"
        ]
        
        for email in invalid_emails:
            otp, reference = "123456", "ABC123"
            success, error = SignupService.send_otp_email(email, otp, reference)
            
            self.assertFalse(success, f"Should fail for email: {email}")
            self.assertEqual(error, "Only @ku.th email addresses are allowed for registration")

    def test_send_otp_email_similar_but_invalid_domain(self):
        """Test sending OTP with an email that looks similar but is not @ku.th"""
        email = "student@faku.th"
        otp, reference = "123456", "ABC123"
        success, error = SignupService.send_otp_email(email, otp, reference)
        
        self.assertFalse(success)
        self.assertEqual(error, "Only @ku.th email addresses are allowed for registration")
        
    def test_send_otp_email_multiple_at_symbols(self):
        """Test sending OTP with emails containing multiple @ symbols"""
        invalid_emails = [
            "student@something@ku.th",
            "invalid@email@ku.th",
            "multiple@@ku.th"
        ]
        
        for email in invalid_emails:
            otp, reference = "123456", "ABC123"
            success, error = SignupService.send_otp_email(email, otp, reference)
            
            self.assertFalse(success, f"Should fail for email: {email}")
            self.assertEqual(error, "Only @ku.th email addresses are allowed for registration")