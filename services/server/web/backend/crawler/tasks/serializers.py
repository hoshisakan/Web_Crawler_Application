from django_celery_results.models import TaskResult
from rest_framework import serializers
from .models import ExtraTaskInfo


class ObtainTaskResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskResult
        fields = ('id', 'task_id', 'status', 'result', 'date_done', 'traceback', 'task_name', 'date_created')

class PastTaskResultSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TaskResult
        fields = ('id', 'task_id', 'status', 'result', 'date_done', 'traceback', 'task_name', 'date_created')

class ExtraTaskInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtraTaskInfo
        # fields = ('id', 'task', 'data_source' , 'data_type', 'last_modify_date', 'created_at')
        fields = ('id', 'task', 'task_mark', 'data_source' , 'data_type', 'last_modify_date', 'created_at')

class ExtraTaskIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtraTaskInfo
        fields = ('task')

class ChangeExtraTaskInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtraTaskInfo
        # fields = ('id', 'username' ,'task', 'task_mark', 'data_source' , 'data_type', 'is_multiple', 'last_modify_date', 'created_at')
        fields = ('id', 'username' ,'task', 'task_mark', 'data_source' , 'data_type', 'is_multiple')

class JoinTaskResultSerializer(serializers.ModelSerializer):
    data_source = serializers.SerializerMethodField()
    data_type = serializers.SerializerMethodField()
    task_mark = serializers.SerializerMethodField()
    is_multiple = serializers.SerializerMethodField()

    class Meta:
        model = TaskResult
        # fields = ('id', 'task_id', 'status', 'result', 'date_done', 'traceback', 'task_name', 'date_created', 'data_type', 'data_source')
        fields = ('id', 'task_id', 'task_mark', 'status', 'result', 'date_done', 'task_name', 'data_type', 'data_source', 'is_multiple')

    def get_data_source(self, obj):
        return ExtraTaskInfo.objects.filter(task=obj.task_id).values('data_source')[0]['data_source']

    def get_data_type(self, obj):
        return ExtraTaskInfo.objects.filter(task=obj.task_id).values('data_type')[0]['data_type']

    def get_task_mark(self, obj):
        return ExtraTaskInfo.objects.filter(task=obj.task_id).values('task_mark')[0]['task_mark']

    def get_is_multiple(self, obj):
        return ExtraTaskInfo.objects.filter(task=obj.task_id).values('is_multiple')[0]['is_multiple']