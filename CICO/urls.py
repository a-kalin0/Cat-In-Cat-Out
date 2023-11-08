from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path("", views.vue, name="index"),
    path("e/", views.PageMotE.as_view(), name="pageE"),
    path("status", views.PageStatus.as_view(), name="status"),
    path("connexion/<int:formId>", views.connection, name ="connexion"),
    path("faq",views.faq, name = "faq"),
    path("contact",views.contact, name = "contact"),
    path("profileIndex", views.profileIndex, name ="profileIndex"),
    path("commande", views.commande, name ="commande"),
    path("forgotpassword", views.forgotpassword, name = "forgotpassword"),
    path("updatepassword/<str:uidb64>/<str:token>/", views.updatepassword, name = "updatepassword"),
    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
]
