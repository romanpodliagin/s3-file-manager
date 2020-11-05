# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import mimetypes

from django.core.files import File as CFile
from django.http import HttpResponse
from django.shortcuts import render
from django.template.context_processors import csrf
from django.views import View
from rest_framework import generics

from file_manager.forms import FileUploadForm
from file_manager.models import File, Directory, Bucket
from file_manager.serializers import DirectorySerializer
from file_manager.utils import S3Helper

s3_helper = S3Helper()


class DIRList(generics.ListAPIView):
    queryset = Directory.objects.all()
    serializer_class = DirectorySerializer


class DIRView(View):

    def get(self, *args, **kwargs):
        dir_object = s3_helper.get_model_by_kwargs(Directory, {'id': kwargs['dir_id']})
        filenames = File.objects.filter(directory=dir_object).order_by('-aws_last_modified')
        nested_dirs = dir_object.nested_directories.filter(nested=True)
        return render(self.request, 'dirs_view.html', {'filenames': filenames, 'nested_dirs': nested_dirs})


class FilesView(View):

    def get(self, *args, **kwargs):
        return render(self.request, 'home.html', {'filenames': Directory.objects.filter(nested=False)})


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
            directory = request.POST['directory']
            dir_object = s3_helper.get_model_by_kwargs(Directory, {'id': int(directory)})

            file_obj_data = s3_helper.load_zip_file(file_obj)
            if file_obj_data:
                for file_obj_item in file_obj_data:

                    if file_obj_item['dir_name']:
                        # replace dir_object with nested_dir
                        nested_dir_object = dir_object.get_or_create_nested_directory(file_obj_item['dir_name'])
                    else:
                        nested_dir_object = dir_object

                    directory_name = f'{nested_dir_object.get_full_dir_path()}'
                    s3_filename = s3_helper.upload_zip_file(file_obj_item, directory_name)
                    new_file = File.objects.create(aws_key=s3_filename, directory=nested_dir_object)
                    new_file.update_attrs(update_keys=['bucket', 'aws_last_modified', 'aws_size'])

                return render(request, 'upload.html', {'alert': {'msg': 'File successfully unzipped:',
                                                                 'filename': file_obj.name}}
                              )
            else:
                s3_filename = s3_helper.upload_file(file_obj, dir_object.name)
                new_file = File.objects.create(aws_key=s3_filename, directory=dir_object)
                new_file.update_attrs(update_keys=['bucket', 'aws_last_modified', 'aws_size'])

                return render(request, 'upload.html', {'alert': {'msg': 'File successfully saved:',
                                                                 'filename': s3_filename}}
                              )


class FileDownload(View):

    def get(self, *args, **kwargs):
        file_id = kwargs['file_id']
        file_name = s3_helper.get_model_attr_by_kwargs(model=File, kwargs={'id': file_id},
                                                       attr_name='aws_key'
                                                       )
        local_file_name = s3_helper.download_file(file_name)
        f = open(local_file_name)
        myFile = CFile(f)
        content_type = mimetypes.guess_type(local_file_name, strict=True)
        response = HttpResponse(myFile, content_type=content_type)
        content = "attachment; filename=%s" % local_file_name
        response['Content-Disposition'] = content
        s3_helper.remove_local_file(local_file_name)
        return response


class BaseUpdateAPIView(generics.UpdateAPIView):

    def check_filename(self, full_file_name, short_file_name) -> dict:
        if File.objects.filter(aws_key=full_file_name).exists():
            return {'msg': 'File or DIR exists.'}

        if not short_file_name:
            return {'msg': 'Name cannot be empty.'}


class DIRCreate(BaseUpdateAPIView):

    def post(self, request, *args, **kwargs):
        dir_name = request.POST['dir_name']

        error_msg = self.check_filename(full_file_name=f'{dir_name}/', short_file_name=dir_name)
        if error_msg:
            return HttpResponse(json.dumps(error_msg), content_type="application/json", status=400)

        bucket = s3_helper.get_model_by_kwargs(Bucket, {'name': s3_helper.aws_storage_bucket_name})

        s3_filename = s3_helper.create_dir(dir_name)
        new_dir = Directory.objects.create(name=s3_filename, bucket=bucket)
        # new_file.update_attrs(update_keys=[])
        return HttpResponse('OK')


class FileRename(BaseUpdateAPIView):

    def post(self, request, format=None):
        file_id = int(request.POST['file_id'])
        file_name = request.POST['file_name']
        file_object = s3_helper.get_model_by_kwargs(File, {'id': file_id})
        new_file_name = f'{file_object.directory.name}' + request.POST['full_file_name']
        
        error_msg = self.check_filename(full_file_name=new_file_name, short_file_name=file_name)
        if error_msg:
            return HttpResponse(json.dumps(error_msg), content_type="application/json", status=400)

        rename_error_msg = file_object.rename_file(new_file_name)
        if rename_error_msg:
            return HttpResponse(json.dumps(rename_error_msg), content_type="application/json", status=400)

        context = {'File': new_file_name}
        return HttpResponse(json.dumps(context), content_type="application/json")


class FileDelete(generics.DestroyAPIView):

    def post(self, request, format=None):
        file_id = int(request.POST['file_id'])
        file_object = s3_helper.get_model_by_kwargs(File, {'id': file_id})
        file_name = file_object.aws_key
        file_object.delete()
        context = {'File': file_name}
        return HttpResponse(json.dumps(context), content_type="application/json")
