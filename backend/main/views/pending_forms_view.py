from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from main.models import Form, User

class PendingFormsView(LoginRequiredMixin, View):
    """
    View to display all pending forms with student information.
    Only accessible to inspectors.
    """
    template_name = 'pending_forms.html'
    
    def get(self, request, *args, **kwargs):
        # Check if the user is an inspector
        if request.user.role != User.Role.INSPECTOR:
            return HttpResponse("Unauthorized", status=403)
        
        # Get all pending forms
        pending_forms = Form.objects.filter(form_status=Form.FormStatus.PENDING)
        
        # Create a list of dictionaries with form information and student code
        forms_data = []
        for form in pending_forms:
            forms_data.append({
                'form_id': form.form_id,
                'form_type': form.form_type,
                'form_status': form.form_status,
                'student_code': form.user_fk.student_code,
                'student_name': form.user_fk.name,
            })
        
        context = {
            'forms_data': forms_data,
        }
        
        return render(request, self.template_name, context)