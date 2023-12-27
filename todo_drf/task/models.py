from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
# Create your models here.
class Tag(models.Model):
    title = models.CharField(max_length=50, unique=True,blank=False)
    objects= models.Manager()

    def __str__(self):
        return self.title

class Task(models.Model):
    title = models.CharField(max_length=100,blank=False, null=False)
    description = models.CharField(max_length=1000,blank=False, null=False)
    Due_date =models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    tag = models.ManyToManyField(Tag,blank=True)
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('WORKING', 'Working'),
        ('DONE', 'Done'),
        ('OVERDUE', 'Overdue'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='OPEN')
    objects= models.Manager()

    def __str__(self):
        return self.title
    
    def clean(self):
        if self.Due_date and self.Due_date < timezone.now().date():
            raise ValidationError("Due date cannot be in the past.")
    