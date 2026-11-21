from django.urls import path

from . import views

app_name = "inventario"
urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("materiales/", views.materiales, name="materiales"),
]
