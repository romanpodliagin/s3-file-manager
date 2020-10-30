"""s3_file_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url
from file_manager import views


urlpatterns = [
    url('home/', views.home, name='home'),
    url('dirs_list/', views.dir_list, name='dir_list'),
    url('dirs/view/(?P<dir_name>.*?)/', views.dir_view, name='dir_view'),
    url('file/upload/', views.upload, name='upload'),
    url('file/rename/(?P<file_name>.*?)/', views.rename, name='upload'),
    url('file/delete/(?P<file_name>.*?)/', views.delete, name='upload')

]
