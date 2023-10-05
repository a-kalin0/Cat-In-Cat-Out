from django.urls import path
from . import views

urlpatterns = [
    path("", views.vue, name="index"),
    path("e/", views.PageMotE.as_view(), name="pageE"),
    path("status", views.PageStatus.as_view(), name="status")
]

def test():
    print("a")