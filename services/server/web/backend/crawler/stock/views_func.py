# from re import U
from django.db.models import Q

class StockInfoViewsFunc():
    def __init__(self, obj):
        self.__models = obj

    def filterRecordsByUsername(self, username):
        return self.__models.objects.filter(username=username)

    def checkInfoExists(self, username, ticker):
        filter_result = self.__models.objects.filter(Q(username=username) & Q(ticker=ticker))
        if filter_result.exists() is False:
            return False, None
        return True, filter_result.values('task')[0]['task']

    def filterInfoByTaskIdUsername(self, username, task_id):
        return self.__models.objects.filter(Q(username=username) & Q(task=task_id))

    def filterInfoByTaskId(self, task_id):
        return self.__models.objects.filter(task=task_id)

    def filterChartInfoAuth(self, username, task_id):
        return self.__models.objects.filter(Q(username=username) & Q(task=task_id))

    def filterChartInfo(self, task_id, search_type):
        return self.__models.objects.filter(task=task_id).values(search_type, 'trade_date')

    def clearRecordsByTaskIdUsername(self, username, task_id):
        filter_result = self.filterInfoByTaskIdUsername(username, task_id)
        if filter_result.exists() is False:
            raise Exception('Not match data records by task id')
        return filter_result.delete()