from django.urls import path

from . import views

app_name = "Cubage"
urlpatterns = [
    #/Cubage/
    path("cartographie/", views.carte, name="carte"),
    path("acceuil/", views.index, name="index"),
    path("information/", views.information, name="information"),
    path("", views.info, name="info"),
]