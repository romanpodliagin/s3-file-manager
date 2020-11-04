from django import forms


class FileUploadForm(forms.Form):
    directory = forms.Select()
    filename = forms.CharField(max_length=50, required=False)
    file = forms.FileField()
