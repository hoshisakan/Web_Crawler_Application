from celery import shared_task, chain, uuid
from .background.google_search_info import GoogleSearchInfo
from crawler.config import Initialization as Init
from module.log_generate import Loggings
from module.handle_exception import HandleException
# from module.handle_file import FileOperation
# import os
# from threading import Thread
# import queue
from module.call_api import APIRequest
import math


logger = Loggings()
# file_operation = FileOperation(path=os.getcwd())


def chain_tasks_run_google_search_crawler(**params):
    task_id = uuid()
    try:
        chain(
                crawler_google_search_info.s(
                    keyword=params['keyword'], page_count=params['page_count'],
                    task_id=task_id, data_type=params['data_type'], auth_user=params['auth_user']),
                handle_crawler_info.s(
                    keyword=params['keyword'], data_type=params['data_type'], task_id=task_id,
                    data_source='google search', auth_token=params['auth_token'], is_multiple=params['is_multiple']
                ),
                task_id=task_id
        )()
    except Exception as e:
        logger.error(HandleException.show_exp_detail_message(e))
    return task_id

@shared_task(ignore_result=True)
def crawler_google_search_info(**task):
    obtain_info = GoogleSearchInfo(
        keyword=task['keyword'],
        page_count=task['page_count'],
        task_id=task['task_id'],
        data_type=task['data_type'],
        auth_user=task['auth_user']
    )
    return obtain_info.scrape()

@shared_task
def handle_crawler_info(result, **crawler):
    threading_result = []
    api_res_for_task = APIRequest(Init.api_endpoint['extra_task'])
    threading_result.append(
    api_res_for_task.postRequest(
        {
            'task': crawler['task_id'], 'data_source': crawler['data_source'],
            'data_type': crawler['data_type'], 'task_mark': crawler['keyword'], 'is_multiple': crawler['is_multiple']
        },
        crawler['auth_token']
        )
    )
    if crawler['data_type'] not in ['google news', 'google video']:
        raise Exception('Unknown data type')

    api_res_for_save_info = APIRequest(Init.api_endpoint['google_search'][crawler['data_type']]['base'])

    if 'json_rows' in result and result['json_rows']:
        write_rows_count = len(result['json_rows'])
        logger.debug(f'rows total: {write_rows_count}')
        threading_result.append(
            api_res_for_save_info.postRequest(
                result['json_rows'],
                crawler['auth_token']
            )
        )
    if not result['json_rows'] or all(threading_result) is False:
        err_msg = f"Task {crawler['task_id']} run threading failed.\nResult: {threading_result}"
        raise Exception(err_msg)
    return threading_result
