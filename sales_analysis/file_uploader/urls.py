# file_uploader/urls.py
from django.urls import path
from . import views

app_name = 'file_uploader'

urlpatterns = [
    path('success/<int:file_id>/', views.upload_success, name='success'),
]