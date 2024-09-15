from django.db import models

# Create your models here.
class CustomUser(models.Model):
    first_name = models.CharField(max_length=50)
    second_name = models.CharField(max_length=50, blank=True, null=True)
    last_name_father = models.CharField(max_length=50)
    last_name_mother = models.CharField(max_length=50, blank=True, null=True)
    age = models.IntegerField()
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128) 

    def __str__(self):
        return f"{self.first_name} {self.last_name_father}"
