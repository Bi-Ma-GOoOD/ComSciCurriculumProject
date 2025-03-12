from django.urls import path

from main.views import FileUploadView
from main.views import GradeVerifyView

urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='file-upload-view'),
    path('credit-verify/', GradeVerifyView.as_view(), name='credit-verify-view')
]