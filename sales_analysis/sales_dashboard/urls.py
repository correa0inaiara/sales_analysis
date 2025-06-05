# sales_dashboard/urls.py
from django.urls import path
from . import views

app_name = 'sales_dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('upload/', views.sales_upload, name='upload'),
    path('analyze/<int:file_id>/', views.analyze_sales, name='analyze'),
    path('results/', views.analysis_results, name='results'),
]