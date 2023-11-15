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
    path("forgotpassword", views.forgotpassword, name ="forgotpassword"),
    path("newpassword/<uidb64>/<token>/", views.newpassword, name="newpassword"),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('mail_sent',views.mail_sent,name="mail_sent"),
    path('reset_done', views.reset_done, name="reset_done")
]
