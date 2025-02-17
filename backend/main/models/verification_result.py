import uuid
from django.db import models

from .form import Form

class VerificationResult(models.Model) :
    
    class VerificationResult(models.IntegerChoices) :
        PASS = 1
        NOT_PASS = 0
        
    verification_result_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    result_status = models.IntegerField(choices=VerificationResult.choices, default=VerificationResult.NOT_PASS)
    activity_status = models.IntegerField(choices=VerificationResult.choices, default=VerificationResult.NOT_PASS)

    form_id = models.ForeignKey(Form, on_delete=models.CASCADE)
    