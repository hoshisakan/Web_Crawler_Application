from django.shortcuts import get_object_or_404
from .models import PttBoardInfo, PttArticlesInfo
from .serializers import ObtainPttBoardInfoSerializer, ChangePttBoardInfoSerializer, \
                        ColumnsPttBoardInfoSerializer, ObtainPttArticlesInfoSerializer, \
                        ChangePttArticlesInfoSerializer, ExportPttArticlesInfoSerializer, \
                        ValidatePttBoardInfoSerializer
from rest_framework import viewsets, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from module.handle_exception import HandleException
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import action
from .views_func import PttArticlesInfoViewsFunc, PttBoarInfoViewsFunc
from module.file_downloader import FileDownloader
from .tasks import chain_tasks_run_ptt_crawler


# Create your views here.
class PttBoardInfoViewset(viewsets.ModelViewSet):
    queryset = PttBoardInfo.objects.all()
    serializer_class = ObtainPttBoardInfoSerializer
    parsers_classes = [JSONParser]

    def get_permissions(self):
        if self.action in ('retrieve', 'destroy', 'update', 'partial_update', 'create'):
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def list(self, request):
        try:
            serializer = self.get_serializer(self.queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e.args[0]),"message": "get data failed."},status=status.HTTP_403_FORBIDDEN)
    
    def create(self, request):
        data = request.data
        try:
            self.serializer_class = ChangePttBoardInfoSerializer
            # many if set True than allow batch write rows to db
            serializer = self.get_serializer(data=data, many=True) if isinstance(data, list) else self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({'message': 'data successfully created'}, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            return Response({"error": e.args[0],"message": "create data failed."},status=status.HTTP_403_FORBIDDEN)
    
    def retrieve(self, request, pk=None):
        try:
            queryset = self.views_func.filterRecordsByUsernameAndId(username=request.user, id=pk)
            instance = get_object_or_404(queryset)
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": e.args[0],"message": "retrieve data failed."},status=status.HTTP_200_OK)

    def update(self, request, pk=None, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            self.serializer_class = ChangePttBoardInfoSerializer
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response({'is_update': True}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'is_update': False, 'detail': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": e.args[0],"message": "delete data failed."},status=status.HTTP_403_FORBIDDEN)

    @action(methods=['GET'], detail=False, url_path='obtain-list')
    def obtain_board_list(self, request):
        try:
            self.serializer_class = ColumnsPttBoardInfoSerializer
            serializer = self.get_serializer(self.queryset, many=True)
            # data = serializer.data
            # result = []
            # for read in data:
            #     temp = {}
            #     temp['id'] = read['name']
            #     temp['value'] = read['name']
            #     result.append(temp)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e.args[0])}, status=status.HTTP_403_FORBIDDEN)

class PttArticlesInfoViewset(viewsets.ModelViewSet):
    queryset = PttArticlesInfo.objects.all()
    serializer_class = ObtainPttArticlesInfoSerializer
    parsers_classes = [JSONParser]
    views_func = PttArticlesInfoViewsFunc(PttArticlesInfo)
    views_func_ptt_board = PttBoarInfoViewsFunc(PttBoardInfo)

    def get_permissions(self):
        if self.action in ('destroy', 'update', 'partial_update'):
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def list(self, request):
        try:
            self.queryset = self.views_func.filterRecordsByUsername(username=request.user)
            serializer = self.get_serializer(self.queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e.args[0]),"message": "get data failed."},status=status.HTTP_403_FORBIDDEN)
    
    def create(self, request):
        data = request.data
        try:
            self.serializer_class = ChangePttArticlesInfoSerializer
            # many if set True than allow batch write rows to db
            serializer = self.get_serializer(data=data, many=True) if isinstance(data, list) else self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({'message': 'data successfully created'}, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            return Response({"error": e.args[0],"message": "create data failed."},status=status.HTTP_403_FORBIDDEN)
    
    def retrieve(self, request, pk=None):
        try:
            queryset = self.views_func.filterRecordsByUsernameAndId(username=request.user, id=pk)
            instance = get_object_or_404(queryset)
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": e.args[0],"message": "retrieve data failed."},status=status.HTTP_200_OK)

    def update(self, request, pk=None, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            queryset = self.views_func.filterRecordsByUsernameAndId(username=request.user, id=pk)
            instance = get_object_or_404(queryset)
            self.serializer_class = ChangePttArticlesInfoSerializer
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response({'is_update': True}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'is_update': False, 'detail': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            queryset = self.views_func.filterRecordsByUsernameAndId(username=request.user, id=pk)
            instance = get_object_or_404(queryset)
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": e.args[0],"message": "delete data failed."},status=status.HTTP_403_FORBIDDEN)

    @action(methods=['POST'], detail=False, url_path='obtain-info')
    def obtain_info(self, request):
        data = request.data
        try:
            action_mode = data.get('action_mode', None)
            board_name = data.get('board_name', None)
            search_keyword = data.get('search_keyword', None)
            search_page_count = data.get('search_page_count', None)
            search_page_limit_enable = data.get('search_page_limit_enable', None)

            if any(list(dict(data).values())) is False:
                raise Exception('action_mode, board_name, search_keyword, search_page_count, search_page_limit_enable is required.')
            if action_mode is None:
                raise Exception("The action mode is required.")
            elif action_mode is not None and action_mode not in ['Page', 'Keyword']:
                raise Exception("Invalid action mode.")
            else:
                if action_mode and action_mode == 'Page':
                    if not board_name or not search_page_count:
                        raise Exception("Search page count and board name is required.")
                    if isinstance(search_page_count, str) and search_page_count.isdigit() is False:
                        raise Exception("Invalid search page count.")
                    elif int(search_page_count) < 1:
                        raise Exception("Search page count and board name is required.")
                elif action_mode and action_mode == 'Keyword':
                    if not search_keyword or search_page_limit_enable is None or not board_name:
                        raise Exception("Invalid search keyword or search page limit enable or board_name.")
                    if search_page_limit_enable is True:
                        if not search_page_count:
                            raise Exception("Invalid search page count.")
                        if isinstance(search_page_count, str) and search_page_count.isdigit() is False:
                            raise Exception("Invalid search page count.")
                        elif int(search_page_count) < 1:
                            raise Exception("Search page count and board name is required.")
            data['search_page_count'] = int(search_page_count)
            board_queryset = self.views_func_ptt_board.filterRecordByName(name=board_name)
            board_serializer = ValidatePttBoardInfoSerializer(board_queryset, many=True)
            board_serializer_data = board_serializer.data[0]
            base_url = board_serializer_data['url']
            if base_url:
                data['base_url'] = base_url

            auth_token = request.headers.get('Authorization').split(' ')[1]
            is_multiple = True if isinstance(data, list) and len(data) > 1 else False
            task_id = chain_tasks_run_ptt_crawler(
                data=data,
                auth_token=auth_token,
                auth_user=str(request.user),
                is_multiple=is_multiple
            )
            return Response({'task_id': task_id}, status=status.HTTP_200_OK)
        except Exception as e:
            print({'error': str(e.args[0])})
            print(data)
            return Response({'error': str(e.args[0])}, status=status.HTTP_403_FORBIDDEN)
    
    @action(detail=False, methods=['GET'], url_path='filter-info')
    def filter_info(self, request):
        data = request.query_params
        try:
            task_id = data.get('task_id', None)
            if task_id is None:
                raise Exception({'task id': ['The field is required.']})
            self.queryset = self.views_func.filterInfoByTaskIdUsername(task_id=task_id, username=request.user)
            serializer = self.get_serializer(self.queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": e.args[0],"message": "get data failed."},status=status.HTTP_403_FORBIDDEN)
    
    @action(methods=['DELETE'], detail=False, url_path='remove-info')
    def remove_search_info_by_task_id(self, request):
        data = request.data
        try:
            task_id = data.get('task_id', None)
            if task_id is None:
                raise Exception("{'task id': ['The field is required.']}")
            delete_result = self.views_func.clearRecordsByTaskIdUsername(task_id=task_id, username=request.user)
            return Response({'is_deleted': True, 'detail': delete_result}, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response({'error': str(e.args[0])}, status=status.HTTP_403_FORBIDDEN)
    
    @action(detail=False, methods=['GET'], url_path='export-info')
    def export_specific_file(self, request):
        data = request.query_params
        try:
            task_id = data.get('task_id', None)
            export_type = data.get('export_type', None)

            if task_id is None or export_type is None:
                raise Exception(
                    {
                        'task id': ['The field is required.'],
                        'export type': ['The field is required.'],
                    }
                )

            self.serializer_class = ExportPttArticlesInfoSerializer
            file_downloader = FileDownloader()
            cols = ['name', 'title' ,'url', 'push_count', 'author', 'date', 'page']
            self.queryset = self.views_func.filterInfoByTaskIdUsername(task_id=task_id, username=request.user)

            if export_type == 'csv':
                serializer = self.get_serializer(self.queryset, many=True)
                export_data = serializer.data
                export_response = file_downloader.export_csv_by_http_response(
                    filename=task_id,
                    cols=cols,
                    rows=export_data
                )
            elif export_type == 'json':
                serializer = self.get_serializer(self.queryset, many=True)
                export_response = file_downloader.export_json_by_http_response_v2(
                    filename=task_id,
                    rows=serializer.data
                )
            return export_response
        except Exception as e:
            return Response({"error": str(e.args[0]),"message": "get data failed."},status=status.HTTP_403_FORBIDDEN)