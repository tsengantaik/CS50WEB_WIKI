from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.findentry, name="findentry"),
    path("search", views.search, name="search"),
    path("addnewpage", views.addnewpage, name="addnewpage"),
    path("edit/<str:titlename>", views.edit, name="edit"),
    path("random", views.theone, name="random")
]
