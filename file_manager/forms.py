from django import forms


class FileUploadForm(forms.Form):
    filename = forms.CharField(max_length=50)
    file = forms.FileField()