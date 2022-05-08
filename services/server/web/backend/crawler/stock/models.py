from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class StockInfo(models.Model):
    task = models.TextField(null=False, blank=False)
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stock_items', null=False, blank=False, to_field='username')
    ticker = models.CharField(max_length=50)
    open_price = models.DecimalField(max_digits=7, decimal_places=2, null=False, blank=False)
    high_price = models.DecimalField(max_digits=7, decimal_places=2, null=False, blank=False)
    low_price = models.DecimalField(max_digits=7, decimal_places=2, null=False, blank=False)
    close_price = models.DecimalField(max_digits=7, decimal_places=2, null=False, blank=False)
    adj_close_price = models.DecimalField(max_digits=7, decimal_places=2, null=False, blank=False)
    volume = models.BigIntegerField(null=False, blank=False)
    trade_date = models.DateField(null=False, blank=False)
    last_modify_date = models.DateTimeField(auto_now=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'stock_info'
        app_label = 'stock'