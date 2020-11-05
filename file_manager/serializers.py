from rest_framework import serializers

from file_manager.models import Directory


class DirectorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(label='Price', source='get_full_dir_path')

    class Meta:
        model = Directory
        fields = ('id', 'name')
