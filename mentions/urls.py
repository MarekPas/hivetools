from django.urls import path
from . import views

urlpatterns = [
    path('', views.mentions_manager, name='mentions-manager'),
]