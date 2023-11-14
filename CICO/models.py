from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db.models import UniqueConstraint


class UserCICO(AbstractUser):
    ownedDevice = models.CharField(max_length=100, unique=True, null=True)

class ToDoItem(models.Model):
    text = models.CharField(max_length=100)
    due_date = models.DateField(default=timezone.now)

class CiCoItem(models.Model):
    text = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.text}"
# Create your models here.

class Statuses(models.Model):
    status = models.CharField(max_length=100)
    hour = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.status} à {self.hour}"
    
class Cat(models.Model):
    image_front = models.ImageField(upload_to='images/')
    image_back = models.ImageField(upload_to='images/')
    image_right = models.ImageField(upload_to='images/')
    image_left = models.ImageField(upload_to='images/')
    name = models.CharField(max_length=100)


class UserSettings(models.Model):
    userId = models.OneToOneField(UserCICO, primary_key=True, on_delete=models.PROTECT)
    setting1 = models.CharField(max_length=100)
    #add other settings as required

class DeviceRecords(models.Model):
    deviceId = models.ForeignKey(UserCICO, to_field="ownedDevice", on_delete=models.PROTECT)
    recordId = models.AutoField(primary_key=True)
    UniqueConstraint(fields=['deviceId', 'recordId'], name='composite_PK')
    time = models.DateTimeField(auto_now_add=True)

    EVENTS_CHOICES = [
        ("IN", "Entrée"),
        ("OUT", "Sortie"),
    ]
    event = models.CharField(max_length=3, choices=EVENTS_CHOICES)
    isCat = models.BooleanField()

class Cats(models.Model):
    ...
    ownerId = models.ForeignKey(UserCICO, on_delete=models.CASCADE)
    catId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    #add other details if needed


class Trigger(models.Model):
    ...
    catId = models.ForeignKey(Cats, on_delete=models.CASCADE)
    recordId = models.ForeignKey(DeviceRecords,primary_key=True,  to_field="recordId", on_delete=models.CASCADE)
