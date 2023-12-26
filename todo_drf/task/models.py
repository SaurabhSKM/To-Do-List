from django.db import models

# Create your models here.
class Tag(models.Model):
    title = models.CharField(max_length=50, unique=True)
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
    