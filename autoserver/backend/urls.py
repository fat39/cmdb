"""autoserver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.urls import path,re_path
from django.contrib import admin
from backend import views

urlpatterns = [
    re_path(r'^curd.html$', views.curd),
    re_path(r'^curd_json.html$', views.curd_json),
    re_path(r'^asset.html$', views.asset),
    re_path(r'^asset_json.html$', views.asset_json),
    re_path(r'^idc.html$', views.idc),
    re_path(r'^idc_json.html$', views.idc_json),


]
