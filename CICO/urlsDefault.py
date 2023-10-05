from django.urls import path
from . import views

urlpatterns = [
    path("", views.Empty),
    path("void", views.Void.as_view(), name="test")
]