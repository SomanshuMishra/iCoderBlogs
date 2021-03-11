from django.db import models
from datetime import datetime
# Create your models here.

class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=13)
    email = models.EmailField(max_length=254)
    content = models.TextField(max_length=300)
    # timeStamp = models.DateTimeField('datetime.now')
    
    def __str__(self):
        return  'Message from ' + self.name
     