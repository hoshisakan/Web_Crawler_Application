from django.http.response import HttpResponse
import csv
import json
from django.core import serializers


class FileDownloader():
    def __init__(self):
        pass

    def export_csv_by_http_response(self, **export):
        response = HttpResponse(content_type='text/csv')
        export_filename = export['filename']
        response['Content-Disposition'] = f'attachment; filename="{export_filename}.csv"'
        response.write(u'\ufeff'.encode('utf-8'))
        writer = csv.writer(response, delimiter=',')
        write_rows = []

        if export['rows'] is not None or not export['rows']:
            write_rows = [list(field.values()) for field in export['rows']]
        write_rows.insert(0, export['cols'])
        writer.writerows(write_rows)
        return response

    def export_csv_by_stream_response(self):
        pass

    # 缺點是匯出檔案時會連同 model name 與 pk value
    def export_json_by_http_response_v1(self, **export):
        """use serializers.serialize method convert object to json str, then convert to http response"""
        # method 1
        json_str = serializers.serialize("json", export['queryset'], indent=4, fields=export['cols'])
        # method 2
        # JSONSerializer = serializers.get_serializer("json")
        # json_serializer = JSONSerializer()
        # json_serializer.serialize(export['queryset'], indent=4, fields=export['cols'])
        # json_str = json_serializer.getvalue()
        response = HttpResponse(json_str, content_type='application/json')
        export_filename = export['filename']
        response['Content-Disposition'] = f'attachment; filename="{export_filename}.json"'
        return response

    def export_json_by_http_response_v2(self, **export):
        """use json dumps convert dict to str, then convert to http response"""
        json_str = json.dumps(export['rows'], indent=4, ensure_ascii=False)
        response = HttpResponse(json_str, content_type='application/json')
        export_filename = export['filename']
        response['Content-Disposition'] = f'attachment; filename="{export_filename}.json"'
        return response