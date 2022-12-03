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
from bridge.stu import views as stu_views

urlpatterns = [
    path('login/', stu_views.login),
    path('register/', stu_views.register),
    path('modify/', stu_views.modify),
    path('add/', stu_views.add),
    path('getinfo/', stu_views.getinfo),
    path('mycourse/', stu_views.myCourse),
    path('rmcourse/', stu_views.delete),
    path('changepasswd/', stu_views.changePasswd),
    path('rate/', stu_views.rateCourse),
    path('comment/', stu_views.makeComment),
    path('deletecomment/', stu_views.delComment),
    path('newthemepost/', stu_views.newThemePost),
    path('deletethemepost/', stu_views.deleteThemePost),
    path('newfollowpost/', stu_views.newFollowPost),
    path('deletefollowpost/', stu_views.deleteFollowPost),
]
