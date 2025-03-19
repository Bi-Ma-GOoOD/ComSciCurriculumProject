import uuid
from django.db import models

from .user import User

class Form(models.Model) :
    
    class FormStatus(models.TextChoices) :
        READY_TO_CALC = 'ready to calc'
        DRAFT =  'draft'
        PENDING = 'pending'
        VERIFIED = 'verified'
        
    class FormType(models.TextChoices) :
        CREDIT_CHECK = 'credit check'
        GRADUATION_CHECK = 'graduation check'
        
    form_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    form_status = models.CharField(max_length=20, choices=FormStatus.choices, default=FormStatus.DRAFT)
    form_type = models.CharField(max_length=20, choices=FormType.choices, default=FormType.GRADUATION_CHECK)
    
    user_fk = models.ForeignKey(User, on_delete=models.CASCADE)
