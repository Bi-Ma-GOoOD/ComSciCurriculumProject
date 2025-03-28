import uuid
from django.test import TestCase
from main.models import User, Form, VerificationResult, CreditDetail
from main.services.login_service import LoginService

class LoginServiceTest(TestCase):
    
    def setUp(self):
        """Set up test data"""
        # Create a STUDENT user
        self.student_user = User.objects.create(
            email='student@ku.th',
            password='password123',
            name='Student User',
            student_code='6410500001',
            role=User.Role.STUDENT
        )
        
        # Create a form for the STUDENT
        self.student_form = Form.objects.create(
            form_status=Form.FormStatus.DRAFT,
            form_type=Form.FormType.GRADUATION_CHECK,
            user_fk=self.student_user
        )
        
        # Create an INSPECTOR user
        self.inspector_user = User.objects.create(
            email='inspector@ku.th',
            password='password123',
            name='Inspector User',
            role=User.Role.INSPECTOR
        )
    
    def test_authenticate_user_success(self):
        """Test successful authentication"""
        success, user = LoginService.authenticate_user('student@ku.th', 'password123')
        self.assertTrue(success)
        self.assertEqual(user.email, 'student@ku.th')
        self.assertEqual(user.role, User.Role.STUDENT)
        
    def test_authenticate_user_wrong_password(self):
        """Test authentication with wrong password"""
        success, message = LoginService.authenticate_user('student@ku.th', 'wrongpassword')
        self.assertFalse(success)
        self.assertEqual(message, "Invalid email or password")
        
    def test_authenticate_user_not_found(self):
        """Test authentication with non-existent user"""
        success, message = LoginService.authenticate_user('nonexistent@ku.th', 'password123')
        self.assertFalse(success)
        self.assertEqual(message, "User not found")
        
    def test_authenticate_user_empty_fields(self):
        """Test authentication with empty fields"""
        success, message = LoginService.authenticate_user('', '')
        self.assertFalse(success)
        self.assertEqual(message, "Email and password are required")
        
    def test_authenticate_user_non_ku_email(self):
        """Test authentication with non-KU email"""
        success, message = LoginService.authenticate_user('user@example.com', 'password123')
        self.assertFalse(success)
        self.assertEqual(message, "Only @ku.th email addresses are allowed")
        
    def test_get_user_form(self):
        """Test getting user form"""
        form = LoginService.get_user_form(self.student_user)
        self.assertIsNotNone(form)
        self.assertEqual(form.form_type, Form.FormType.GRADUATION_CHECK)
        
    def test_get_redirect_url_graduation_check(self):
        """Test redirect URL for graduation check form"""
        grad_form = Form.objects.create(
            form_type=Form.FormType.GRADUATION_CHECK,
            user_fk=self.student_user
        )
        url = LoginService.get_redirect_url(grad_form)
        self.assertEqual(url, '/insertGradFile/')
        
    def test_get_redirect_url_credit_check(self):
        """Test redirect URL for credit check form"""
        # Create a credit check form
        credit_form = Form.objects.create(
            form_status=Form.FormStatus.DRAFT,
            form_type=Form.FormType.CREDIT_CHECK,
            user_fk=self.student_user
        )
        url = LoginService.get_redirect_url(credit_form)
        self.assertEqual(url, '/creditCheck/')
        
    def test_get_redirect_url_no_form(self):
        """Test redirect URL with no form"""
        url = LoginService.get_redirect_url(None)
        self.assertEqual(url, '/fileAttachCheck/')