from django.db import models

# Create your models here.


class Contact(models.Model):
    contact = models.CharField(max_length=50,null=True)
    display_name = models.CharField(max_length=250,null=True)


    

