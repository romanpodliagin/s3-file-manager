# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.core.files import File as CFile
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.template.context_processors import csrf
from django.views import View
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view

from file_manager.forms import FileUploadForm
from file_manager.models import File
from file_manager.utils import S3Client

s3_client = S3Client()


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


class DIRView(View):

    def get(self, *args, **kwargs):
        dir_object = File.objects.get(id=kwargs['dir_id'])
        filenames = File.objects.filter(Q(aws_key__contains=dir_object.aws_key),
                                        ~Q(id=kwargs['dir_id'])
                                        )

        return render(self.request, 'home.html', {'filenames': filenames})


class FilesView(View):

    def get(self, *args, **kwargs):
        return render(self.request, 'home.html', {'filenames': File.objects.all()})


class FileUpload(generics.CreateAPIView):

    def get(self, request):
        form = FileUploadForm()
        context = {}
        context.update(csrf(request))
        context['form'] = form
        return render(request, 'upload.html', context)

    def post(self, request):
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file_obj = request.FILES['file']
            s3_filename = s3_client.upload_file(file_obj)

            new_file = File.objects.create(aws_key=s3_filename)
            new_file.update_attrs(update_keys=['bucket', 'aws_last_modified', 'aws_size'])

            return render(request, 'upload.html', {'alert': {'msg': 'File successfully saved:',
                                                             'filename': s3_filename}}
                          )


class FileDownload(View):

    def get(self, *args, **kwargs):
        file_id = kwargs['file_id']
        file_object = File.objects.get(id=file_id)
        file_name = file_object.aws_key
        local_file_name = s3_client.download_file(file_name)

        f = open(local_file_name)
        myFile = CFile(f)
        response = HttpResponse(myFile, content_type='application/x-gzip')
        content = "attachment; filename=%s" % local_file_name
        response['Content-Disposition'] = content
        s3_client.remove_local_file(local_file_name)
        return response


@api_view()
def rename(request, file_name):
    return HttpResponse('U OK')


class FileDelete(generics.DestroyAPIView):

    def post(self, request, format=None):
        file_id = int(request.POST['file_id'])
        file_object = File.objects.get(id=file_id)
        file_name = file_object.aws_key
        s3_client.delete_file(file_name)
        file_object.delete()
        context = {'File': file_name}
        return HttpResponse(json.dumps(context), content_type="application/json")


@api_view()
def create_dir(request):
    return HttpResponse('U OK')
