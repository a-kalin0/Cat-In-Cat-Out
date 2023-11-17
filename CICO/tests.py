import django.test
from django.test import TestCase
from django.urls import reverse
from .models import UserCICO
from .models import Cats
from .models import DeviceRecords
from .models import Trigger
from django.template.loader import render_to_string
from django.contrib.auth import login
import math




def createSession():
    testClient = django.test.Client(REMOTE_ADDR='127.0.0.1')
    testSession = testClient.session
    testSession['IP'] = "127.0.0.1"
    testSession.save()
    return testClient, testSession

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


        response = client.get(reverse('profileIndex'))
        #print(response.context["recordList"][0]["recordId"])


        self.assertQuerySetEqual(
            str(response.context["recordList"][0]["recordId"]),
            str(newRecord.recordId)
        )

    def testDisplayOnProfileIndex(self):
        """
        Tests that the list displays upon entering profileIndex by testing that a table row appears if there's a cat record
        """
        testClient, testSession = createSession()


        testUser = UserCICO.objects.create_user('my-user-name', password="testpwd", ownedDevice=12)
        self.assertTrue(testClient.login(username='my-user-name', password="testpwd"))
        testCat = Cats.objects.create(ownerId=testUser, name="testCat")
        testRecord = DeviceRecords.objects.create(deviceId=testUser, event="IN", isCat=True)
        testTrigger = Trigger.objects.create(catId=testCat, recordId=testRecord)

        response = testClient.get(reverse('profileIndex'))

        self.assertContains(response, '<tr id=row_1>')

    def testListContainsAll(self):
        """
        Tests that the list obtained by the page contains all records when going through all pages of the list
        """
        testClient, testSession = createSession()
        testSession['listStart'] = 0
        testUser = UserCICO.objects.create_user('my-user-name', password="testpwd", ownedDevice=12)
        self.assertTrue(testClient.login(username='my-user-name', password="testpwd"))
        testCat = Cats.objects.create(ownerId=testUser, name="testCat")
        testRecord = DeviceRecords.objects.create(deviceId=testUser, event="IN", isCat=True)
        testTrigger = Trigger.objects.create(catId=testCat, recordId=testRecord)

        testRecord2 = DeviceRecords.objects.create(deviceId=testUser, event="OUT", isCat=True)
        Trigger.objects.create(catId=testCat, recordId=testRecord2)

        testRecord3 = DeviceRecords.objects.create(deviceId=testUser, event="IN", isCat=True)
        Trigger.objects.create(catId=testCat, recordId=testRecord3)
        response = testClient.get(reverse('profileIndex'))
        testList = []
        for i in range(math.ceil(len(DeviceRecords.objects.all())/2)):
            testSession['listStart'] = i * 2
            for j in range(len(response.context["recordList"])):
                testList.append(response.context["recordList"][j]["recordId"])
            testClient.post(reverse("profileIndex"),{"bouton":"ancien"})
            response = testClient.get(reverse('profileIndex'))

        self.assertEqual(testList, list(DeviceRecords.objects.values_list('recordId', flat=True))[::-1])




