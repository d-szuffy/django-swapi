from django.db import models
from django.dispatch import receiver
from django.core.signals import request_started
import os
# Create your models here.


class DataSet(models.Model):
    filename = models.CharField(max_length=100)
    file_path = models.FilePathField()
    created_at = models.DateTimeField(auto_now_add=True)
    edited_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.filename

    def __repr__(self):
        return "Filename: {0}, located at: {1}".format(self.filename, self.file_path)
