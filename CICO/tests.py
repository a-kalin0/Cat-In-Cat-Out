import django.test
from django.test import TestCase
from django.urls import reverse
from .models import CiCoItem
from .models import UserCICO
from .models import Cats
from .models import DeviceRecords
from .models import Trigger
from django.contrib.auth import login



def create_item(text):
    return CiCoItem.objects.create(text=text)


class AllTest(TestCase):

    def test(self):
        client = django.test.Client(REMOTE_ADDR='127.0.0.1')

        user = UserCICO.objects.create_user('my-user-name', password="testpwd", ownedDevice=12)
        self.assertTrue(client.login(username='my-user-name', password="testpwd"))
        cat = Cats.objects.create(ownerId=user, name="testCat")
        newRecord = DeviceRecords.objects.create(deviceId=user, event="IN", isCat=True)

        newTrigger = Trigger.objects.create(catId=cat, recordId=newRecord)
        print(cat)
        session = client.session
        session['IP'] = "127.0.0.1"
        session.save()


        response = client.get(reverse('profileIndex', kwargs={'listButton':"None"}))
        #print(response.context["recordList"][0]["recordId"])


        self.assertQuerySetEqual(
            str(response.context["recordList"][0]["recordId"]),
            str(newRecord.recordId)
        )

