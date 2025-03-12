import uuid
from django.db import models

from .credit_detail import CreditDetail
from .subcategory import Subcategory
from .category import Category

class SubcategoryDetails(models.Model) :
    subcategory_detail_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    acquired_credit = models.IntegerField()
    
    subcateory_fk = models.ForeignKey(Subcategory, on_delete=models.CASCADE, null=True, blank=True)
    category_fk = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    credit_details_fk = models.ForeignKey(CreditDetail, on_delete=models.CASCADE)