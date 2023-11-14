from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [

    path("", views.vue, name="index"),
    path("e/", views.PageMotE.as_view(), name="pageE"),
    path("status", views.PageStatus.as_view(), name="status"),
    path("connexion/<int:formId>", views.connection, name ="connexion"),
    path("faq",views.faq, name = "faq"),
    path("contact",views.contact, name = "contact"),
    path("profileIndex", views.profileIndex, name ="profileIndex"),
    path("commande", views.commande, name ="commande"),
    path('add_cat/', views.add_cat, name='add_cat'),
    path('get_cats/', views.get_cats, name='get_cats'),




] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)