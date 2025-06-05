# inventory_dashboard/urls.py
from django.urls import path
from . import views

app_name = 'inventory_dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('upload/', views.inventory_upload, name='upload'),
    path('analyze/<int:file_id>/', views.analyze_inventory, name='analyze'),
]