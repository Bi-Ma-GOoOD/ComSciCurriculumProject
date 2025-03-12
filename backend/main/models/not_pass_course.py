import uuid
from django.db import models

from .credit_detail import CreditDetail
from .enrollment import Enrollment

class NotPassCourse(models.Model) :
    not_pass_course_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    
    credit_detail_fk = models.ForeignKey(CreditDetail, on_delete=models.CASCADE)
    enrollment_fk = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'credit_detail_fk: {self.credit_detail_fk}, enrollment_fk: {self.enrollment_fk}'