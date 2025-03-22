from main.models import Form

class ViewPendingFormsService:
    """
    Unified service class for handling form operations
    """
    
    @staticmethod
    def get_pending_forms():
        """Get all pending forms"""
        # Use __in to filter for multiple statuses
        pending_forms = Form.objects.filter(
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