from django.urls import path
from main.views import GradeVerifyView, signup_view, otp_verify_view, user_signup_view, login_view, CalculateView, FileUploadView

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('verify-otp/', otp_verify_view, name='verify-otp'),
    path('register/', user_signup_view, name='register'),
    path('login/', login_view, name='login'),
    path('upload/', FileUploadView.as_view(), name='file-upload-view'),
    path('credit-verify/', GradeVerifyView.as_view(), name='credit-verify-view'),
    path('calculate/', CalculateView.as_view(), name='calculate-view'),
]