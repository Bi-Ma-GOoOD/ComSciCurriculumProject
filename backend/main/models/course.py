from django.db import models

from .subcategory import Subcategory

class Course(models.Model) :
    course_id = models.CharField(primary_key=True, max_length=11)
    credit = models.IntegerField()
    course_name_th = models.CharField(max_length=200)
    course_name_en = models.CharField(max_length=200)
    
    subcategory_fk = models.ForeignKey(Subcategory, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f"{self.course_id} - {self.course_name_th} - {self.course_name_en}"