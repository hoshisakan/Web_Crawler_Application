from .models import PttBoardInfo, PttArticlesInfo
from rest_framework import serializers
from django.utils.timezone import now


class ObtainPttBoardInfoSerializer(serializers.ModelSerializer):
    days_since_created = serializers.SerializerMethodField()
    class Meta:
        model = PttBoardInfo
        fields = ('id', 'name', 'classify' ,'url', 'days_since_created')

    def get_days_since_created(self, obj):
        return (now() - obj.created_at).days

class ChangePttBoardInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PttBoardInfo
        fields = ('id', 'name', 'classify' ,'url')

class ColumnsPttBoardInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PttBoardInfo
        fields = ('id', 'name', 'classify')

class ValidatePttBoardInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PttBoardInfo
        fields = ('name', 'url')

class ObtainPttArticlesInfoSerializer(serializers.ModelSerializer):
    days_since_created = serializers.SerializerMethodField()
    class Meta:
        model = PttArticlesInfo
        fields = ('id', 'task', 'name', 'title' ,'url', 'push_count', 'author', 'date', 'page', 'days_since_created')

    def get_days_since_created(self, obj):
        return (now() - obj.created_at).days

class ChangePttArticlesInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PttArticlesInfo
        fields = ('id', 'task', 'username', 'name', 'title' ,'url', 'push_count', 'author', 'date', 'page')

class ExportPttArticlesInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PttArticlesInfo
        fields = ('name', 'title' ,'url', 'push_count', 'author', 'date', 'page')