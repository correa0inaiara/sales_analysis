"""
URL configuration for sales_analysis project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render

def home_view(request):
    """Página inicial com opções de dashboards"""
    return render(request, 'home.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, 'home.html'),

    path('upload/', include('file_uploader.urls')),
    path('sales/', include('sales_dashboard.urls')),
    path('inventory/', include('inventory_dashboard.urls')),
    # path('debug/', views.debug_interface_html, name='debug_html'),
    # path('debug/json/', views.debug_interface, name='debug_json'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)