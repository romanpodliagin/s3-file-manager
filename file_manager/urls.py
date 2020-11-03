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
    url('file/upload/', views.FileUpload.as_view(), name='file_upload'),
    url('file/download/(?P<file_id>.*?)$', views.FileDownload.as_view(), name='file_download'),
    url('file/rename/$', views.FileRename.as_view(), name='file_rename'),
    url('file/delete/$', views.FileDelete.as_view(), name='file_delete'),

    url('dirs/view/(?P<dir_id>.*?)$', views.DIRView.as_view(), name='dir_view'),
    url('dirs/create/$', views.DIRCreate.as_view(), name='dir_create'),

    # url('dirs_list/', views.dir_list, name='dir_list'),
    # url('api/', include('file_manager.api.urls')),

    url('$', views.FilesView.as_view(), name='home'),

]
