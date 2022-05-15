from django.db import models
from django.core.validators import URLValidator
# from django_celery_results.models import TaskResult
from django.contrib.auth.models import User

class GoogleNewsSearch(models.Model):
    task = models.TextField()
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='google_search_news_items', null=False, blank=False, to_field='username')
    keyword = models.CharField(max_length=50, null=False, blank=False)
    title = models.CharField(max_length=1024, null=False, blank=False)
    summary = models.CharField(max_length=1024, null=False, blank=False)
    updated_time = models.CharField(max_length=15, null=False, blank=True)
    url = models.CharField(max_length=1024, validators=[URLValidator], null=False, blank=False)
    newspaper = models.CharField(max_length=50, null=False, blank=True)
    search_page = models.IntegerField()
    last_modify_date = models.DateTimeField(auto_now=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'google_search_news_info'
        app_label = 'google_search'

class GoogleVideoSearch(models.Model):
    task = models.TextField()
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='google_search_video_items', null=False, blank=False, to_field='username')
    keyword = models.CharField(max_length=50, null=False, blank=False)
    title = models.CharField(max_length=1024, null=False, blank=False)
    summary = models.CharField(max_length=1024, null=False, blank=True)
    updated_time = models.CharField(max_length=30, null=False, blank=True)
    url = models.CharField(max_length=1024, validators=[URLValidator], null=False, blank=True)
    uploader = models.CharField(max_length=60, null=False, blank=True)
    video_length = models.CharField(max_length=30, null=False, blank=True)
    search_page = models.IntegerField()
    last_modify_date = models.DateTimeField(auto_now=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'google_search_video_info'
        app_label = 'google_search'