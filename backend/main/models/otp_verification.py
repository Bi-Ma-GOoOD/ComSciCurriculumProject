from django.db import models
import random
import uuid

class OTPVerification(models.Model):
    otp_verification_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    email = models.EmailField()  # Temporary email storage
    otp = models.CharField(max_length=6)
    reference_otp = models.CharField(max_length=20, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    @classmethod  
    def generate_otp(cls):  
        return str(random.randint(100000, 999999))
    
    @classmethod
    def generate_reference(cls):
        return str(uuid.uuid4().hex[:16])