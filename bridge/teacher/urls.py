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
from bridge.teacher import views as teacher_views

urlpatterns = [
    path('login/', teacher_views.login),
    path('register/', teacher_views.register),
    path('modify/', teacher_views.modify),
    path('add/', teacher_views.add),
    path('getinfo/', teacher_views.getinfo),
    path('mycourse/', teacher_views.myCourse),
    path('rmcourse/', teacher_views.delete),
    path('changepasswd/', teacher_views.changePasswd),
    path('addmaterial/', teacher_views.addMaterial),
    path('newthemepost/', teacher_views.newThemePost),
    path('deletethemepost/', teacher_views.deleteThemePost),
    path('newfollowpost/', teacher_views.newFollowPost),
    path('deletefollowpost/', teacher_views.deleteFollowPost),

]
