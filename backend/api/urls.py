from django.urls import path
from main.views import FileUploadView
from main.views import GradeVerifyView, PendingFormsView, signup_view, otp_verify_view, user_signup_view, login_view

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('verify-otp/', otp_verify_view, name='verify-otp'),
    path('register/', user_signup_view, name='register'),
    path('login/', login_view, name='login'),
    path('upload/', FileUploadView.as_view(), name='file-upload-view'),
    path('credit-verify/', GradeVerifyView.as_view(), name='credit-verify-view'),
    path('pending-forms/', PendingFormsView.as_view(), name='pending-forms-view'),
]