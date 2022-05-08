from rest_framework import viewsets, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from .models import StockInfo
from .serializers import ObtainStockInfoSerializer, ChangeStockInfoSerializer \
                        ,ExportStockInfoSerializer, OpenPriceSerializer \
                        ,HighPriceSerializer, LowPriceSerializer \
                        ,ClosePriceSerializer, AdjClosePriceSerializer \
                        ,VolumePriceSerializer
from .views_func import StockInfoViewsFunc
from module.file_downloader import FileDownloader
from rest_framework.permissions import IsAdminUser, IsAuthenticated
# from module.call_api import APIRequest
# from crawler.config import Initialization as Init
from .tasks import chain_tasks_run_stock_crawler
# from module.handle_exception import HandleException as help
# from module.date import DateTimeTools as DT
import collections


# Create your views here.
class StockInfoViewset(viewsets.ModelViewSet):
    queryset = StockInfo.objects.all()
    serializer_class = ObtainStockInfoSerializer
    parser_classes = [JSONParser]
    views_func = StockInfoViewsFunc(StockInfo)

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
            self.serializer_class = ChangeStockInfoSerializer
            # many if set True than allow batch write rows to db
            serializer = self.get_serializer(data=data, many=True) if isinstance(data, list) else self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({'message': 'data successfully created'}, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            return Response({"error": e.args[0],"message": "create data failed."},status=status.HTTP_403_FORBIDDEN)

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

            self.serializer_class = ExportStockInfoSerializer
            file_downloader = FileDownloader()
            cols = [
                    'ticker', 'trade_date', 'open_price', 'high_price', 'low_price',
                    'close_price', 'adj_close_price', 'volume'
                ]
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
        
    @action(detail=False, methods=['GET'], url_path='chart-info')
    def generate_chart_info(self, request):
        data = request.query_params
        try:
            task_id = data.get('task_id', None)
            search_type = data.get('search_type', None)
            filter_condition = data.get('filter_condition', None)

            self.queryset = self.views_func.filterChartInfoAuth(
                task_id=task_id, username=request.user
            )
            serializer_dict = {
                'open_price': OpenPriceSerializer,
                'high_price': HighPriceSerializer,
                'low_price': LowPriceSerializer,
                'close_price': ClosePriceSerializer,
                'adj_close_price': AdjClosePriceSerializer,
                'volume': VolumePriceSerializer,
                'all': ExportStockInfoSerializer
            }
            self.serializer_class = serializer_dict[search_type]
            serializer = self.get_serializer(self.queryset, many=True)
            serializer_data = serializer.data
            result = []

            if filter_condition != 'multiple':
                if search_type != 'volume' and search_type != 'all':
                    [result.append([read['trade_date'], float(read[search_type])]) for index, read in enumerate(serializer_data, 0)] 
                    result = sorted(result, key=lambda x: x[0], reverse=False)
                    result.insert(0, ['Date', serializer_data[0]['ticker']])
                elif search_type == 'volume':
                    [result.append([read['trade_date'], int(read[search_type])]) for index, read in enumerate(serializer_data, 0)]
                    result = sorted(result, key=lambda x: x[0], reverse=False)
                    result.insert(0, ['Date', serializer_data[0]['ticker']])
                else:
                    [result.append([
                        read['trade_date'], float(read['open_price']), float(read['high_price']), float(read['low_price']), float(read['adj_close_price'])
                    ]) for read in serializer_data]
                    result = sorted(result, key=lambda x: x[0], reverse=False)
                    result.insert(0, ['Date', 'open price', 'high price', 'low price', 'adj close price'])
            else:
                temp_dict = {}
                target_ticker = list(dict.fromkeys([read['ticker'] for read in serializer_data]))
                for read in serializer_data:
                    ticker_index = target_ticker.index(read['ticker'])
                    temp_data = list(read.values())
                    if read['trade_date'] not in temp_dict:
                        temp_dict[read['trade_date']] = [0] * (len(target_ticker) + 1)
                        read_save_dict = temp_dict[read['trade_date']]
                        read_save_dict[0] = temp_data[1]
                    read_save_dict = temp_dict[read['trade_date']]
                    read_save_dict[ticker_index + 1] = float(temp_data[-1]) if search_type != 'volume' else int(temp_data[-1])
                result_dict = collections.OrderedDict(sorted(temp_dict.items()))
                result = [*list(result_dict.values())]
                result.insert(0, ['Date', *target_ticker])
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            print(str(e.args[0]))
            return Response({"error": str(e.args[0]),"message": "get data failed."},status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=['POST'], url_path='obtain-info')
    def obtain_info(self, request):
        data = request.data
        try:
            auth_token = request.headers.get('Authorization').split(' ')[1]
            is_multiple = True if isinstance(data, list) and len(data) > 1 else False
            task_id = chain_tasks_run_stock_crawler(
                data=data,
                auth_token=auth_token,
                auth_user=str(request.user),
                is_multiple=is_multiple
            )
            return Response({'task_id': task_id}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e.args[0])}, status=status.HTTP_403_FORBIDDEN)