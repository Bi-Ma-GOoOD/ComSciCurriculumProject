from django.db import models
import uuid

from .curriculum import Curriculum

class Category(models.Model) :
    category_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    category_name = models.CharField(max_length=200)
    category_min_credit = models.IntegerField()
    
    curriculum_fk = models.ForeignKey(Curriculum, on_delete=models.CASCADE)

    def __str__(self):
        return f'course category: {self.category_name}'
