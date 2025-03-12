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
    fee_status = models.IntegerField(choices=VerificationResult.choices, default=VerificationResult.NOT_PASS)

    form_fk = models.ForeignKey(Form, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'result_status: {self.result_status}, activity_status: {self.activity_status}, fee_status: {self.fee_status}'
    