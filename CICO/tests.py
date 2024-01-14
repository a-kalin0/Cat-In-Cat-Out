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
import uuid6
import requests
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile


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
        session = client.session
        session['IP'] = "127.0.0.1"
        session.save()


        response = client.get(reverse('profileIndex'))

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
        for i in range(math.ceil(len(DeviceRecords.objects.all())/5)):
            testSession['listStart'] = i * 5
            for j in range(len(response.context["recordList"])):
                testList.append(response.context["recordList"][j]["recordId"])
            testClient.post(reverse("profileIndex"),{"bouton":"ancien"})
            response = testClient.get(reverse('profileIndex'))

        self.assertEqual(testList, list(DeviceRecords.objects.values_list('recordId', flat=True))[::-1])


class CatDeletionTests(TestCase):
    def setUp(self):
        # Create a user
        self.user = UserCICO.objects.create_user(username='testuser', password='12345')
        self.client = Client()
        self.client.login(username='testuser', password='12345')
                # Create a cat
        self.cat = Cats.objects.create(
            ownerId=self.user,
            name="Test Cat",
            catId=uuid6.uuid7()
        )

        self.delete_url = f'/CICO/delete_cat/{self.cat.catId}/'

    def test_delete_cat(self):
        """ Test deleting an existing cat """
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Cats.objects.count(), 0)

    def test_delete_nonexistent_cat(self):
        """ Test deleting a cat that doesn't exist """
        fake_cat_id = uuid6.uuid7()
        delete_url = f'/CICO/delete_cat/{fake_cat_id}/'
        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 404)

    def test_unauthorized_delete_attempt(self):
        """ Test deleting a cat by a user who doesn't own the cat """
        # Create another user and log in
        other_user = UserCICO.objects.create_user(username='otheruser', password='54321')
        self.client.login(username='otheruser', password='54321')

        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Cats.objects.count(), 1)  # The cat should still exist

class CatAdditionTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserCICO.objects.create_user(username='testuser', password='testpassword')
        self.client.force_login(self.user)
        self.add_cat_url = '/CICO/add_cat/'  # Absolute URL

    def test_add_cat_success(self):
        """ Test successful addition of a cat """

        img_url = 'https://images5.alphacoders.com/325/thumb-1920-325672.jpg'
        image_content, image_name = get_image_from_url(img_url)
        cat_data = {
            'name': 'Test Cat',
            'image': SimpleUploadedFile(image_name, image_content.read(), content_type="image/jpeg"),
            }
        response = self.client.post(self.add_cat_url, cat_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Cats.objects.count(), 1)
        self.assertEqual(Cats.objects.first().name, 'Test Cat')

    def test_add_cat_failure_invalid_data(self):
        """ Test cat addition with invalid data """
        cat_data = {'name': ''}  # Invalid data
        response = self.client.post(self.add_cat_url, cat_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertNotEqual(response.status_code, 201)
        self.assertEqual(Cats.objects.count(), 0)

    def test_add_cat_unauthorized(self):
        """ Test cat addition by unauthorized user """
        self.client.logout()
        cat_data = {'name': 'Unauthorized Cat'}
        response = self.client.post(self.add_cat_url, cat_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertNotEqual(response.status_code, 201)
        self.assertEqual(Cats.objects.count(), 0)

    def test_add_duplicate_cat_name_different_users(self):
        """ Test that different users can add cats with the same name """
        # Add a cat for the first user
        self.add_cat('Test Cat')

        # Create a second user and login
        user2 = UserCICO.objects.create_user(username='testuser2', password='testpassword2')
        self.client.force_login(user2)

        # Try to add a cat with the same name for the second user
        response = self.add_cat('Test Cat')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Cats.objects.filter(name='Test Cat').count(), 2)

    def test_add_duplicate_cat_name_same_user(self):
        """ Test that the same user cannot add two cats with the same name """
        # Add a cat for the first user
        self.add_cat('Test Cat')

        # Try to add another cat with the same name for the same user
        response = self.add_cat('Test Cat')
        self.assertNotEqual(response.status_code, 201)
        self.assertEqual(Cats.objects.filter(name='Test Cat').count(), 1)

    def add_cat(self, cat_name):
        """ Helper method to add a cat with the given name """
        img_url = 'https://images5.alphacoders.com/325/thumb-1920-325672.jpg'
        image_content, image_name = get_image_from_url(img_url)
        cat_data = {
            'name': cat_name,
            'image': SimpleUploadedFile(image_name, image_content.read(), content_type="image/jpeg"),
        }
        return self.client.post(self.add_cat_url, cat_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')



def get_image_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        # Return a BytesIO object and a filename string
        return BytesIO(response.content), 'test_image.jpg'  # 'test_image.jpg' can be any filename with a valid extension
    else:
        raise Exception("Failed to download image")

        
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

 
