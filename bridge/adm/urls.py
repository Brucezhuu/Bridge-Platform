"""Bridge课程平台后端 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from bridge import views
from bridge.adm import views as adm_views

urlpatterns = [
    path('login/', adm_views.login),
    path('register/', adm_views.register),
    path('modify/', adm_views.modify),
    path('add/', adm_views.add),
    path('getinfo/', adm_views.getinfo),
    path('rmcourse/', adm_views.delete),
    path('changepasswd/', adm_views.changePasswd),
    path('addmaterial/', adm_views.addMaterial),
    path('newthemepost/', adm_views.newThemePost),
    path('deletethemepost/', adm_views.deleteThemePost),
    path('newfollowpost/', adm_views.newFollowPost),
    path('deletefollowpost/', adm_views.deleteFollowPost),
]