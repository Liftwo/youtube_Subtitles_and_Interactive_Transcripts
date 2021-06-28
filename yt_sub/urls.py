"""yt_sub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from . import views
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap
# from django.contrib.sitemaps import views

sitemaps = {
    'static': StaticViewSitemap,
}

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('admin/', admin.site.urls),
    # path('homepage/', views.homepage, name='homepage'),
    path('upload/<video_id>/', views.upload, name='upload'),
    path('about/', views.about, name='about'),
    path('collect/', views.collect, name='collect'),
    path('test/', views.test),
    # path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    # path('sitemap.xml', views.index, {'sitemaps':sitemaps, 'template_name':'custom_sitemap.html'}),

]
