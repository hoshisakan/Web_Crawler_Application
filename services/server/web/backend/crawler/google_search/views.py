from .models import GoogleNewsSearch, GoogleVideoSearch
from .serializers import ObtainNewsSerializer, ChangeNewsSerializer \
                        , ExportNewsSerializer, ObtainVideoSerializer \
                        , ChangeVideoSerializer, ExportVideoSerializer
from rest_framework import viewsets, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from .views_func import GoogleSearchNewsViewsFunc, GoogleSearchVideoViewsFunc
from rest_framework.decorators import action, api_view
from .tasks import chain_tasks_run_google_search_crawler
from module.handle_exception import HandleException
from django.shortcuts import get_object_or_404
from module.file_downloader import FileDownloader
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from module.log_generate import Loggings

logger = Loggings()

# Create your views here.
class GoogleSearchNewsViewset(viewsets.ModelViewSet):
    queryset = GoogleNewsSearch.objects.all()
    serializer_class = ObtainNewsSerializer
    parser_classes = [JSONParser]
    views_func = GoogleSearchNewsViewsFunc(GoogleNewsSearch)

    def get_permissions(self):
        if self.action in ('retrieve', 'destroy', 'update', 'partial_update'):
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
            self.serializer_class = ChangeNewsSerializer
            # many if set True than allow batch write rows to db
            serializer = self.get_serializer(data=data, many=True) if isinstance(data, list) else self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({'message': 'data successfully created'}, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            logger.error({"error": e.args[0],"message": "create data failed."})
            return Response({"error": e.args[0],"message": "create data failed."},status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, pk=None):
        try:
            queryset = self.views_func.filterRecordsByUsernameAndId(username=request.user, id=pk)
            instance = get_object_or_404(queryset)
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": e.args[0],"message": "retrieve data failed."},status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        try:
            queryset = self.views_func.filterRecordsByUsernameAndId(username=request.user, id=pk)
            instance = get_object_or_404(queryset)
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": e.args[0],"message": "delete data failed."},status=status.HTTP_403_FORBIDDEN)

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

            self.serializer_class = ExportNewsSerializer
            file_downloader = FileDownloader()
            cols = ['title', 'summary', 'update_time', 'newspaper', 'url', 'search_page']
            # cols = ['task', 'title', 'summary', 'update_time', 'newspaper', 'url', 'search_page']
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

class GoogleSearchVideoViewset(viewsets.ModelViewSet):
    queryset = GoogleVideoSearch.objects.all()
    serializer_class = ObtainVideoSerializer
    parser_classes = [JSONParser]
    views_func = GoogleSearchVideoViewsFunc(GoogleVideoSearch)

    def get_permissions(self):
        if self.action in ('retrieve', 'destroy', 'update'):
            permission_classes = [IsAdminUser]
        else:
            permission_classes = []
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
            self.serializer_class = ChangeVideoSerializer
            # many if set True than allow batch write rows to db
            serializer = self.get_serializer(data=data, many=True) if isinstance(data, list) else self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({'message': 'data successfully created'}, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            logger.error({"error": e.args[0],"message": "create data failed."})
            return Response({"error": e.args[0],"message": "create data failed."},status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, pk=None):
        try:
            queryset = self.views_func.filterRecordsByUsernameAndId(username=request.user, id=pk)
            instance = get_object_or_404(queryset)
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": e.args[0],"message": "retrieve data failed."},status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        try:
            queryset = self.views_func.filterRecordsByUsernameAndId(username=request.user, id=pk)
            instance = get_object_or_404(queryset)
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": e.args[0],"message": "delete data failed."},status=status.HTTP_403_FORBIDDEN)

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

            self.serializer_class = ExportVideoSerializer
            file_downloader = FileDownloader()
            # cols = ['task', 'name', 'price', 'platform', 'free_shipping_option', 'url', 'search_page']
            cols = ['title', 'summary', 'update_time', 'uploader', 'video_length', 'url', 'search_page']
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

class GoogleSearchViewset():
    @api_view(['POST'])
    def obtain_info_by_crawler(request):
        data = request.data
        try:
            search_keyword = data.get('search_keyword', None)
            search_page_count = data.get('search_page_count', None)
            data_type = data.get('data_type', None)
            is_multiple = True if isinstance(data, list) and len(data) > 1 else False
            auth_token = request.headers.get('Authorization').split(' ')[1]
            if search_keyword is None or search_page_count is None or data_type is None:
                raise Exception({'field': ['The search keyword and search page count and data type is required']})
            task_id = chain_tasks_run_google_search_crawler(
                keyword=search_keyword,
                page_count=int(search_page_count),
                data_type=data_type,
                auth_token=auth_token,
                auth_user=str(request.user),
                is_multiple=is_multiple
            )
            return Response({'task_id': task_id}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e.args[0])}, status=status.HTTP_403_FORBIDDEN)