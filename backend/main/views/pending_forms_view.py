from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from main.services.view_pending_forms_service import ViewPendingFormsService

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
        
        # Get pending forms data from service
        forms_data = ViewPendingFormsService.get_pending_forms()
        
        context = {
            'forms_data': forms_data,
        }
        
        return render(request, self.template_name, context)