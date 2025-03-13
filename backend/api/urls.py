from django.urls import path

from main.views import CreditVerifyView, signup_view, otp_verify_view, user_signup_view, login_view

urlpatterns = [
    path('credit-verify/', CreditVerifyView.as_view(), name='credit-verify-view'),
    path('signup/', signup_view, name='signup'),
    path('verify-otp/', otp_verify_view, name='verify-otp'),
    path('register/', user_signup_view, name='register'),
    path('login/', login_view, name='login'),
]