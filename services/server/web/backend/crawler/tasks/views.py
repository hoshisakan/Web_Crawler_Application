from django_celery_results.models import TaskResult
from .models import ExtraTaskInfo
from .serializers import PastTaskResultSerializer, ExtraTaskInfoSerializer \
                        ,JoinTaskResultSerializer, ChangeExtraTaskInfoSerializer \
                        , ExtraTaskIdSerializer
# from rest_framework.decorators import parser_classes
from rest_framework import viewsets, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import action
from .views_func import TaskResultViewsFunc, ExtraTaskViewsFunc
from module.handle_exception import HandleException
from django.shortcuts import get_object_or_404
from .tasks import chain_tasks_run_remove_info
from module.log_generate import Loggings

logger = Loggings()

# Create your views here.
class TasksResultViewset(viewsets.ModelViewSet):
    queryset = TaskResult.objects.all()
    serializer_class = PastTaskResultSerializer
    parser_classes = [JSONParser]
    views_func = TaskResultViewsFunc(TaskResult)
    extra_task_views_func = ExtraTaskViewsFunc(ExtraTaskInfo)

    def get_permissions(self):
        if self.action in ('list', 'retrieve', 'destroy', 'update'):
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def list(self, request):
        try:
            self.queryset = self.views_func.sortTaskById()
            serializer = self.get_serializer(self.queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": e.args[0],"message": "get data failed."},status=status.HTTP_403_FORBIDDEN)
    
    def retrieve(self, request, pk=None):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": e.args[0],"message": "retrieve data failed."},status=status.HTTP_403_FORBIDDEN)
    
    def destroy(self, request, pk=None):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": e.args[0],"message": "delete data failed."},status=status.HTTP_403_FORBIDDEN)
        
    @action(methods=['GET'], detail=False, url_path='filter-info')
    def filter_info(self, request):
        data = request.query_params
        try:
            field = data.get('field', None)
            condition = data.get('condition', None)
            if field is None or condition is None:
                raise Exception({'field': ['The field and condition is required']})
            self.queryset = self.views_func.filterField(field=field, condition=condition)
            serializer = self.get_serializer(self.queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e.args[0])}, status=status.HTTP_403_FORBIDDEN)

    @action(methods=['GET'], detail=False, url_path='join-info')
    def join_info(self, request):
        data = request.query_params
        try:
            data_source = data.get('data_source', None)
            data_type = data.get('data_type', None)
            user = str(request.user)

            if data_type is None and data_source is None:
                raise Exception('Field data_type and data_source is required.')
            
            if data_source is not None and data_type is not None:
                queryset = TaskResult.objects.raw(f'''
                    SELECT * FROM django_celery_results_taskresult AS a1 INNER JOIN extra_task_info AS a2 ON a1.task_id = a2.task
                    WHERE a2.data_source = '{data_source}' AND a2.data_type = '{data_type}' AND a2.username_id = '{user}' ORDER BY date_done DESC;
                ''')
            elif data_source is not None and data_type is None or not data_type:
                queryset = TaskResult.objects.raw(f'''
                    SELECT * FROM django_celery_results_taskresult AS a1 INNER JOIN extra_task_info AS a2 ON a1.task_id = a2.task
                    WHERE a2.data_source = '{data_source}' AND a2.username_id = '{user}' ORDER BY date_done DESC;
                ''')
            elif data_type is not None and data_source is None or not data_source:
                queryset = TaskResult.objects.raw(f'''
                    SELECT * FROM django_celery_results_taskresult AS a1 INNER JOIN extra_task_info AS a2 ON a1.task_id = a2.task
                    WHERE a2.data_type = '{data_type}' AND a2.username_id = '{user}' ORDER BY date_done DESC;
                ''')
            serializer = JoinTaskResultSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': e.args[0]}, status=status.HTTP_403_FORBIDDEN)

    @action(methods=['DELETE'], detail=False, url_path='remove-info')
    def remove_task_all_info(self, request):
        data = request.data
        try:
            task_id = data.get('task_id', None)
            auth_token = request.headers.get('Authorization').split(' ')[1]
            if task_id is None:
                raise Exception({'task id': ['The field is required.']})
            queryset = self.views_func.filterByTaskId(task_id=task_id)
            if queryset is False:
                raise Exception('Not found mathch task id.')
            task_status = queryset.values('status')[0]['status']
            instance = get_object_or_404(queryset)
            self.perform_destroy(instance)

            extra_task_queryset = self.extra_task_views_func.filterByTaskIdUsername(task_id=task_id, username=request.user)
            extra_task_queryset_val = extra_task_queryset.values('data_source', 'data_type')[0]
            data_source = extra_task_queryset_val['data_source']
            data_type = extra_task_queryset_val['data_type']
            extra_task_queryset.delete()
            
            if task_status is not None and task_status == "SUCCESS":
                chain_tasks_run_remove_info(
                    remove_task_id=task_id,
                    data_type=data_type,
                    data_source=data_source,
                    auth_token=auth_token
                )
            return Response({'is_deleted': True}, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response({'error': str(e.args[0])}, status=status.HTTP_403_FORBIDDEN)

    @action(methods=['GET'], detail=False, url_path='filter-single-task')
    def filter_single_task_records(self, request):
        data = request.query_params
        try:
            task_id = data.get('task_id', None)
            if task_id is None:
                raise Exception({'task_id': ['The field is required.']})
            self.queryset = self.views_func.filterByTaskId(task_id=task_id)
            serializer = self.get_serializer(self.queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e.args[0])}, status=status.HTTP_403_FORBIDDEN)

class ExtraTaskInfoViewset(viewsets.ModelViewSet):
    queryset = ExtraTaskInfo.objects.all()
    serializer_class = ExtraTaskInfoSerializer
    parser_classes = [JSONParser]
    views_func = ExtraTaskViewsFunc(ExtraTaskInfo)

    def get_permissions(self):
        if self.action in ('retrieve', 'destroy', 'update'):
            permission_classes = [IsAdminUser]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]

    def list(self, request):
        try:
            self.queryset = self.views_func.filterByUsername(username=request.user)
            serializer = self.get_serializer(self.queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": e.args[0],"message": "get data failed."},status=status.HTTP_403_FORBIDDEN)
    
    def create(self, request):
        data = request.data
        try:
            data['username'] = str(request.user)
            self.serializer_class = ChangeExtraTaskInfoSerializer
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({'message': 'data successfully created'}, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            return Response({"error": e.args[0],"message": "get data failed."},status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, pk=None):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": e.args[0],"message": "retrieve data failed."},status=status.HTTP_403_FORBIDDEN)
    
    def destroy(self, request, pk=None):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": e.args[0],"message": "delete data failed."},status=status.HTTP_403_FORBIDDEN)
    
    @action(methods=['DELETE'], detail=False, url_path='remove-task')
    def remove_task(self, request):
        data = request.data
        try:
            data['username'] = request.user
            queryset = self.views_func.filterByTaskIdAndMark(data=data)
            if not queryset or queryset is None:
                raise Exception("No match task id or other condition.")
            instance = get_object_or_404(queryset)
            self.perform_destroy(instance)
            return Response({'is_deleted': True }, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            err_msg = {'error': HandleException.show_exp_detail_message(e)}
            logger.error(err_msg)
            return Response(err_msg, status=status.HTTP_403_FORBIDDEN)

    @action(methods=['DELETE'], detail=False, url_path='remove-info')
    def remove_record_by_task_id(self, request):
        data = request.data
        try:
            task_id = data.get('task_id', None)
            if task_id is None:
                raise Exception("{'task id': ['The field is required.']}")
            queryset = self.views_func.filterByTaskIdUsername(task_id=task_id, username=request.user)
            instance = get_object_or_404(queryset)
            self.perform_destroy(instance)
            return Response({'is_deleted': True}, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response({'error': str(e.args[0])}, status=status.HTTP_403_FORBIDDEN)

    @action(methods=['GET'], detail=False, url_path='filter-single-task')
    def filter_single_task_records(self, request):
        data = request.query_params
        try:
            task_id = data.get('task_id', None)
            if task_id is None:
                raise Exception({'task_id': ['The field is required.']})
            self.queryset = self.views_func.filterByTaskId(task_id=task_id)
            serializer = self.get_serializer(self.queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e.args[0])}, status=status.HTTP_403_FORBIDDEN)