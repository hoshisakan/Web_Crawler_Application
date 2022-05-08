from django.db.models import Q

class PttBoarInfoViewsFunc():
    def __init__(self, obj):
        self.__models = obj

    def filterRecordByName(self, name):
        return self.__models.objects.filter(name=name)

class PttArticlesInfoViewsFunc():
    def __init__(self, obj):
        self.__models = obj

    def filterRecordsByUsername(self, username):
        return self.__models.objects.filter(username=username)

    def filterRecordsByUsernameAndId(self, username, id):
        return self.__models.objects.filter(Q(username=username) & Q(id=id))

    def filterInfoByTaskIdUsername(self, username, task_id):
        return self.__models.objects.filter(Q(username=username) & Q(task=task_id))

    def clearRecordsByTaskIdUsername(self, username, task_id):
        filter_result = self.filterInfoByTaskIdUsername(username, task_id)
        if filter_result.exists() is False:
            raise Exception('Not match data records by task id')
        return filter_result.delete()