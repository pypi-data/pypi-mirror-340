"""
This file defines routing for each plugin view.
"""
from django.urls import path
from . import views

# this must be named same as the plugin
app_name = "interface_relationship_manager"

urlpatterns = [
    path('select-device/', views.select_device_for_split, name='select_device'),
]
