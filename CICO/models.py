from django.db import models
from django.utils import timezone


class ToDoItem(models.Model):
    text = models.CharField(max_length=100)
    due_date = models.DateField(default=timezone.now)

class CiCoItem(models.Model):
    text = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.text}"
# Create your models here.

class TableStatus(models.Model):
    status = models.CharField(max_length=100)
    heure = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return f"{self.status} à {self.heure}"

