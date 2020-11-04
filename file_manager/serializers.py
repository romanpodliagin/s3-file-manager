from rest_framework import serializers

from file_manager.models import Directory


class DirectorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Directory
        fields = ('id', 'name')
