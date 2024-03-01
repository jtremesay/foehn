from django.urls import path

from foehn import views

app_name = "foehn"
urlpatterns = [
    path(f"", views.index, name="index"),
]
