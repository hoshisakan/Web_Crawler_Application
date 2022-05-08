from django.db import models
from django.core.validators import URLValidator
from django.contrib.auth.models import User


# Create your models here.
class PttBoardInfo(models.Model):
    name = models.CharField(unique=True, max_length=50, null=False, blank=False)
    classify = models.CharField(max_length=10, null=False, blank=False)
    url = models.CharField(unique=True, max_length=1024, validators=[URLValidator], null=False, blank=False)
    last_modify_date = models.DateTimeField(auto_now=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'ptt_board_info'
        app_label = 'ptt'

class PttArticlesInfo(models.Model):
    task = models.TextField(null=False, blank=False)
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ptt_article_user_items', null=False, blank=False, to_field='username')
    name = models.ForeignKey(PttBoardInfo, on_delete=models.CASCADE, related_name='ptt_article_board_items', null=False, blank=False, to_field='name')
    title = models.CharField(max_length=80, null=False, blank=False)
    url = models.CharField(max_length=1024, validators=[URLValidator], null=False, blank=False)
    push_count = models.IntegerField()
    author = models.CharField(max_length=25, null=False, blank=False)
    date = models.CharField(max_length=5, null=False, blank=False)
    page = models.IntegerField()
    last_modify_date = models.DateTimeField(auto_now=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)


    class Meta:
        db_table = 'ptt_articles_info'
        app_label = 'ptt'