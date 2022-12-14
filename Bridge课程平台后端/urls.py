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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('stu/', include('bridge.stu.urls')),
    path('teacher/', include('bridge.teacher.urls')),
    path('adm/', include('bridge.adm.urls')),
    path('show/', views.showAllCourse),
    path('search/', views.searchByName),
    path('showcoursecomment/', views.showCourseComment),
    # path('showalltp/', views.showAllTp),
    path('stu/showalltp/', views.showAllTp_stu),
    path('teacher/showalltp/', views.showAllTp_teacher),
    path('showallfp/', views.showAllFp),
    path('searchtp/', views.searchTp),
    path('showcoursematerial/', views.showCourseMaterial),

]
