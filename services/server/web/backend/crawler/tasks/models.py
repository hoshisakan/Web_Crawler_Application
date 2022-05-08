from django.db import models
# from django_celery_results.models import TaskResult
from django.contrib.auth.models import User


# Create your models here.
class ExtraTaskInfo(models.Model):
    task = models.CharField(
        null=False,
        blank=False,
        unique=True,
        max_length=1024
    )
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='extra_task_items', null=False, blank=False, to_field='username')
    task_mark = models.CharField(max_length=50, null=False, blank=False)
    data_source = models.CharField(max_length=50, null=False, blank=False)
    data_type = models.CharField(max_length=50, null=False, blank=False)
    is_multiple = models.BooleanField(null=False, blank=False, default=False)
    last_modify_date = models.DateTimeField(auto_now=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'extra_task_info'
        app_label = 'tasks'