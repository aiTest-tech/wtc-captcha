from django.db import models

# Create your models here.
from django.db import models

class TextData(models.Model):
    content = models.TextField()
    lang = models.CharField(max_length=10, default='en')  # For storing language codes like 'en', 'fr', etc.
    project = models.CharField(max_length=100, default='CMO-SWAR')

    ############
    name = models.CharField(max_length=100, blank=True, null=True)
    occupation = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)  # For storing phone numbers
    district_corporation = models.CharField(max_length=100, blank=True, null=True)
    taluka_zone = models.CharField(max_length=100, blank=True, null=True)
    village_area = models.CharField(max_length=100, blank=True, null=True)
    subject = models.CharField(max_length=200, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)  # Email validation
    mode = models.CharField(max_length=50, blank=True, null=True)
    ############

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:50]