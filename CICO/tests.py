from django.test import TestCase, Client
from django.urls import reverse
from .models import UserCICO
from .models import Cats
from .models import DeviceRecords
from .models import Trigger
from django.template.loader import render_to_string
from django.contrib.auth import login
import math
from .models import Cats, CatsAdventures
from django.utils import timezone



def createSession():
    testClient = Client(REMOTE_ADDR='127.0.0.1')
    testSession = testClient.session
    testSession['IP'] = "127.0.0.1"
    testSession.save()
    return testClient, testSession

class AllTest(TestCase):

    def test(self):
        client = Client(REMOTE_ADDR='127.0.0.1')

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



class TestsGraphiquesDesChats(TestCase):

    def setUp(self):
        self.utilisateur = UserCICO.objects.create_user('utilisateur_test', password="testpwd")
        self.url = reverse('profileIndex')

    def testDisplaysOnProfileIndex(self):
        """
        Tests that the graphics for cat entries and exits appear on the profile page.
        """
        self.client.force_login(self.utilisateur)
        session = self.client.session
        session['IP'] = '127.0.0.1'
        session.save()
        response = self.client.get(self.url)
        self.assertContains(response, '<canvas id="EntreesCat"')
        self.assertContains(response, '<canvas id="SortiesCat"')

    def testCorrectGraphicData(self):
        """
        Tests that the correct data for cat graphs are included in the HTML.
        """
        self.client.force_login(self.utilisateur)
        session = self.client.session
        session['IP'] = '127.0.0.1'
        session.save()
        response = self.client.get(self.url)

        # Récupérez les données attendues
        expected_data = CatsAdventures.objects.filter(
            cat__ownerId=self.utilisateur
        ).values('timestamp', 'entrees', 'sorties')

        # Testez si les scripts nécessaires sont présents
        self.assertContains(response, 'var xValues = ')
        self.assertContains(response, 'var barColors = ')
        self.assertContains(response, 'var catData = ')

        # Vérifiez si les données attendues sont présentes dans la réponse
        for data in expected_data:
            # Formattez la date et les valeurs comme elles apparaîtraient dans le HTML
            formatted_date = data['timestamp'].strftime("%Y-%m-%d")
            formatted_entrees = str(data['entrees'])
            formatted_sorties = str(data['sorties'])

            # Vérifiez si ces valeurs sont présentes dans la réponse
            self.assertContains(response, formatted_date)
            self.assertContains(response, formatted_entrees)
            self.assertContains(response, formatted_sorties)
