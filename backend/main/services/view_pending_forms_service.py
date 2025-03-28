from main.models import Form, User

class ViewPendingFormsService:
    """
    Unified service class for handling form operations
    """
    
    @staticmethod
    def get_pending_forms():
        """Get all pending forms"""
        # Use __in to filter for multiple statuses
        pending_forms = Form.objects.filter(
            form_type=Form.FormType.GRADUATION_CHECK,
            form_status__in=[Form.FormStatus.PENDING, Form.FormStatus.VERIFIED]
        ).select_related('user_fk')
        
        # Create a list of dictionaries with form information and student code
        forms_data = []
        for form in pending_forms:
            forms_data.append({
                'form_id': form.form_id,
                'form_type': form.form_type,
                'form_status': form.form_status,
                'student_code': form.user_fk.student_code,
                'student_name': form.user_fk.name
            })
        
        return forms_data
    
    @staticmethod
    def mock_user_form():
        """Mock user form data"""
        from django.db import transaction
        
        try:
            with transaction.atomic():
                # Check if user already exists
                user, created = User.objects.get_or_create(
                    email='john.doe@ku.th',
                    defaults={
                        'password': '12345678',  # Use a proper hashed password
                        'name': 'John Doe',
                        'student_code': '6012345678',
                        'role': User.Role.STUDENT,
                    }
                )
                
                # Check if form already exists
                Form.objects.get_or_create(
                    user_fk=user,
                    form_status=Form.FormStatus.PENDING,
                    form_type=Form.FormType.GRADUATION_CHECK
                )
                
                print(f"User created/retrieved: {user}")
                print(f"Forms for user: {Form.objects.filter(user_fk=user).count()}")
        
        except Exception as e:
            print(f"Error in mock_user_form: {e}")
            raise