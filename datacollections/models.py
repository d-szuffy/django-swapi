from django.db import models

# Create your models here.


class DataSet(models.Model):
    filename = models.CharField(max_length=100)
    file = models.FilePathField()
    created_at = models.DateTimeField(auto_now_add=True)
    edited_on = models.DateTimeField(auto_now=True)
