from .models import StockInfo
from rest_framework import serializers
from django.utils.timezone import now

class ObtainStockInfoSerializer(serializers.ModelSerializer):
    days_since_created = serializers.SerializerMethodField()
    class Meta:
        model = StockInfo
        fields = (
            'id', 'task', 'ticker' ,'open_price', 'high_price',
            'low_price', 'close_price', 'adj_close_price', 'volume',
            'trade_date','last_modify_date', 'created_at', 'days_since_created')

    def get_days_since_created(self, obj):
        return (now() - obj.created_at).days

class ChangeStockInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockInfo
        fields = (
            'task', 'username', 'ticker' ,'open_price', 'high_price',
            'low_price', 'close_price', 'adj_close_price', 'volume',
            'trade_date')

class ExportStockInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockInfo
        fields = (
            'ticker', 'trade_date', 'open_price', 'high_price',
            'low_price', 'close_price', 'adj_close_price', 'volume')

class OpenPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockInfo
        fields = ('ticker', 'trade_date', 'open_price')

class HighPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockInfo
        fields = ('ticker', 'trade_date', 'high_price')

class LowPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockInfo
        fields = ('ticker', 'trade_date', 'low_price')

class ClosePriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockInfo
        fields = ('ticker', 'trade_date', 'close_price')

class AdjClosePriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockInfo
        fields = ('ticker', 'trade_date', 'adj_close_price')

class VolumePriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockInfo
        fields = ('ticker', 'trade_date', 'volume')