from .models import GoogleNewsSearch, GoogleVideoSearch
from rest_framework import serializers
from django.utils.timezone import now

class ObtainNewsSerializer(serializers.ModelSerializer):
    days_since_created = serializers.SerializerMethodField()
    class Meta:
        model = GoogleNewsSearch
        fields = ('id', 'task', 'keyword' ,'title', 'summary', 'updated_time', 'newspaper', 'url', 'search_page', 'last_modify_date', 'created_at', 'days_since_created')

    def get_days_since_created(self, obj):
        return (now() - obj.created_at).days

class ChangeNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoogleNewsSearch
        fields = ('id', 'task' , 'username' ,'keyword', 'title', 'summary', 'updated_time', 'newspaper', 'url', 'search_page')

class ExportNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoogleNewsSearch
        fields = ('title', 'summary', 'updated_time', 'newspaper', 'url', 'search_page')

class ObtainVideoSerializer(serializers.ModelSerializer):
    days_since_created = serializers.SerializerMethodField()
    class Meta:
        model = GoogleVideoSearch
        fields = ('id', 'task', 'keyword', 'title', 'summary', 'updated_time', 'uploader', 'video_length', 'url', 'search_page', 'last_modify_date', 'created_at', 'days_since_created')

    def get_days_since_created(self, obj):
        return (now() - obj.created_at).days

class ChangeVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoogleVideoSearch
        fields = ('id', 'task', 'username', 'keyword', 'title', 'summary', 'updated_time', 'uploader', 'video_length', 'url', 'search_page')

class ExportVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoogleVideoSearch
        fields = ('title', 'summary', 'updated_time', 'uploader', 'video_length', 'url', 'search_page')