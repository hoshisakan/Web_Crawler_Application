from django.db.models import Q


class GoogleSearchNewsViewsFunc:
    def __init__(self, models):
        self.__models = models

    def filterRecordsByUsername(self, username):
        return self.__models.objects.filter(username=username)

    def filterRecordsByUsernameAndId(self, username, id):
        return self.__models.objects.filter(Q(username=username) & Q(id=id))

    def filterNewsInfoByKeywords(self, keyword):
        """
        Filter google search news info by keyword
        """
        filterResult = self.__models.objects.filter(keyword=keyword)
        return filterResult if filterResult.exists() else []

    def checkTitleExists(self, title, task):
        return self.__models.objects.filter(Q(task=task) & Q(title=title)).exists()

    def filterInfoByTaskId(self, task_id):
        return self.__models.objects.filter(Q(task=task_id))
    
    def filterInfoByTaskIdUsername(self, username, task_id):
        return self.__models.objects.filter(Q(username=username) & Q(task=task_id))
    
    def clearRecordsByTaskId(self, task_id):
        filter_result = self.__models.objects.filter(task=task_id)
        if filter_result.exists() is False:
            raise Exception('No match data records by task id')
        return filter_result.delete()

    def clearRecordsByTaskIdUsername(self, task_id, username):
        filter_result = self.__models.objects.filter(Q(task=task_id) & Q(username=username))
        if filter_result.exists() is False:
            raise Exception('No match data records by task id')
        return filter_result.delete()

    def checkInfoExists(self, username, keyword):
        filter_data = self.__models.objects.filter(Q(username=username) & Q(keyword=keyword))
        if filter_data.exists() is False:
            return False, None
        return True, filter_data.values('task')[0]['task']



class GoogleSearchVideoViewsFunc:
    def __init__(self, models):
        self.__models = models
    
    def filterRecordsByUsername(self, username):
        return self.__models.objects.filter(username=username)

    def filterRecordsByUsernameAndId(self, username, id):
        return self.__models.objects.filter(Q(username=username) & Q(id=id))

    def filterNewsInfoByKeywords(self, keyword):
        """
        Filter google search news info by keyword
        """
        filterResult = self.__models.objects.filter(keyword=keyword)
        return filterResult if filterResult.exists() else []

    def checkTitleExists(self, title, task):
        return self.__models.objects.filter(Q(task=task) & Q(title=title)).exists()

    def filterInfoByTaskId(self, task_id):
        return self.__models.objects.filter(Q(task=task_id))
    
    def filterInfoByTaskIdUsername(self, username, task_id):
        return self.__models.objects.filter(Q(username=username) & Q(task=task_id))
    
    def clearRecordsByTaskId(self, task_id):
        filter_result = self.__models.objects.filter(task=task_id)
        if filter_result.exists() is False:
            raise Exception('No match data records by task id')
        return filter_result.delete()
    
    def clearRecordsByTaskIdUsername(self, task_id, username):
        filter_result = self.__models.objects.filter(Q(task=task_id) & Q(username=username))
        if filter_result.exists() is False:
            raise Exception('No match data records by task id')
        return filter_result.delete()
    
    def checkInfoExists(self, username, keyword):
        filter_data = self.__models.objects.filter(Q(username=username) & Q(keyword=keyword))
        if filter_data.exists() is False:
            return False, None
        return True, filter_data.values('task')[0]['task']