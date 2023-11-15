from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db.models import UniqueConstraint
from django.core.exceptions import ValidationError
import uuid



class UserCICO(AbstractUser):
    ownedDevice = models.CharField(max_length=100, unique=True, null=True)


# Create your models here.

class Statuses(models.Model):
    status = models.CharField(max_length=100)
    hour = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.status} à {self.hour}"
    

class UserSettings(models.Model):
    userId = models.OneToOneField(UserCICO, primary_key=True, on_delete=models.PROTECT)
    setting1 = models.CharField(max_length=100)
    #add other settings as required

class DeviceRecords(models.Model):
    deviceId = models.ForeignKey(UserCICO, to_field="ownedDevice", on_delete=models.PROTECT,name="deviceId")
    recordId = models.AutoField(primary_key=True)
    time = models.DateTimeField(auto_now_add=True)

    EVENTS_CHOICES = [
        ("IN", "Entrée"),
        ("OUT", "Sortie"),
    ]
    event = models.CharField(max_length=3, choices=EVENTS_CHOICES)
    isCat = models.BooleanField()

def cat_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'media/user_{0}/cat_{1}/{2}'.format(instance.ownerId_id, instance.catId, filename)

class Cats(models.Model):
    ...
    ownerId = models.ForeignKey(UserCICO, on_delete=models.CASCADE)
    catId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=cat_directory_path, null=True, blank=True)
    #add other details if needed

    def clean(self):
        if Cats.objects.filter(name=self.name).exists():
            raise ValidationError("A cat with this name already exists for this user.")
                                  
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class Trigger(models.Model):
    catId = models.ForeignKey(Cats, on_delete=models.CASCADE, to_field="catId", name="catId")
    recordId = models.ForeignKey(DeviceRecords,primary_key=True,  to_field="recordId", on_delete=models.CASCADE, name = "recordId")
