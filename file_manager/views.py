# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

from file_manager.forms import FileUploadForm
from file_manager.utils import S3Client

s3_client = S3Client()


@api_view()
def home(request):
    response = [{
        'dirs_list': request.build_absolute_uri(f'/dirs_list/'),
        'create_dir': request.build_absolute_uri(f'/dirs/create/'),
        'upload_file': request.build_absolute_uri(f'/file/upload/')
    }
    ]
    return Response(response)


@api_view()
def dir_list(request):
    dirs = s3_client.list_dir()
    dirs_dict = {}

    for dir_name in dirs:
        dirs_dict[dir_name] = {'dir_name': dir_name,
                               'view': request.build_absolute_uri(f'/dirs/view/{dir_name}'),
                               'delete': request.build_absolute_uri(f'/dirs/delete/{dir_name}')
                               }

    return Response([dirs_dict])


@api_view()
def dir_view(request, dir_name):
    filenames = s3_client.list_dir_by_name(dir_name)
    response = []

    for filename in filenames:
        response.append({filename: {'name': filename,
                                    'file/rename': request.build_absolute_uri(f'/file/rename/{filename}'),
                                    'file/delete': request.build_absolute_uri(f'/file/delete/{filename}')
                                    }
                         }
                        )
    return Response(response)


@api_view()
def upload(request):
    form = FileUploadForm()
    # s3_client.upload_file(filename)
    # 'requirements.txt'
    return render(request, 'upload.html', {'form': form})


@api_view()
def rename(request, file_name):
    return HttpResponse('U OK')


@api_view()
def delete(request, file_name):
    return HttpResponse('U OK')


@api_view()
def create_dir(request):
    return HttpResponse('U OK')
