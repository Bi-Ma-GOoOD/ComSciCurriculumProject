from django.urls import path

from main.views import GradeVerifyView

urlpatterns = [
    path('credit-verify/', GradeVerifyView.as_view(), name='credit-verify-view')
]