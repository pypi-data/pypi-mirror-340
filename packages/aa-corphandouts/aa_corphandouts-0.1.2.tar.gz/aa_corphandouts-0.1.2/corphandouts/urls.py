"""Routes."""

from django.urls import path

from . import views

app_name = "corphandouts"

urlpatterns = [
    path("", views.index, name="index"),
    path("doctrine/<int:doctrine_id>", views.doctrine, name="doctrine"),
    path("fitting/<int:fitting_id>", views.fitting, name="fitting"),
    path("modal_loader_body", views.modal_loader_body, name="modal_loader_body"),
]
