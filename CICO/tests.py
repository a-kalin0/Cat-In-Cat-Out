from django.test import TestCase
from django.urls import reverse
from .models import CiCoItem



def create_item(text):
    return CiCoItem.objects.create(text=text)


class AllTest(TestCase):

    def test_no_e(self):
        todo = create_item("word")
        response = self.client.get(reverse("index"))
        self.assertQuerySetEqual(
            response.context["cicoitem_list"],
            [todo]
        )

    def test_with_e(self):
        todo = create_item("word")
        response = self.client.get(reverse("pageE"))
        self.assertQuerySetEqual(
            response.context["cicoitem_list"],
            []
        )

