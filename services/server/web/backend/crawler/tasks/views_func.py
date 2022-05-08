from django.db.models import Q
# from module.log_generate import Loggings

# logger = Loggings()

class ExtraTaskViewsFunc:
    def __init__(self, models):
        self.__models = models

    def filterByTaskId(self, task_id):
        return self.__models.objects.filter(task=task_id)

    def filterByUsername(self, username):
        return self.__models.objects.filter(username=username)

    def filterByTaskIdUsername(self, task_id, username):
        return self.__models.objects.filter(Q(task=task_id) & Q(username=username))

    def filterByKeywordUsername(self, keyword, username):
        return self.__models.objects.filter(Q(keyword=keyword) & Q(username=username))

    def filterByTaskIdAndMark(self, data={}):
        return self.__models.objects.filter(
            Q(username=data['username']) & (Q(task=data['task_id']) | (Q(task_mark=data['task_mark']) & Q(data_source=data['data_source']) & Q(data_type=data['data_type'])))
        )


class TaskResultViewsFunc:
    def __init__(self, models):
        self.__models = models

    def filterField(self, field, condition):
        if field == "status":
            return self.__models.objects.filter(status=condition).order_by("-date_created")
        elif field == "date_done":
            return self.__models.objects.filter(date_done__date=condition).order_by("-date_created")

    def sortTaskById(self):
        return self.__models.objects.order_by("-id")
    
    def filterByTaskId(self, task_id):
        filter_result = self.__models.objects.filter(task_id=task_id)
        check_exists = filter_result.exists()
        if check_exists is True:
            return filter_result
        return check_exists

    def filterByTaskIdUsername(self, task_id, username):
        return self.__models.objects.filter(Q(task_id=task_id) & Q(username=username))