from celery import shared_task, chain, uuid
from .background.ptt_info_obtain import PttInfoObtain
from crawler.config import Initialization as Init
from module.log_generate import Loggings
from module.handle_exception import HandleException
from module.call_api import APIRequest
from module.date import DateTimeTools as DT
from threading import Thread
import queue

logger = Loggings()
# file_operation = FileOperation(path=os.getcwd())

def chain_tasks_run_ptt_crawler(data, auth_token, auth_user, is_multiple):
    task_id = uuid()
    logger.info(f'Starting ptt info crawler task id: {task_id}')
    try:
        chain(
            crawler_ptt_info.s(
                params=data,
                auth_user=auth_user,
                task_id=task_id),
            handle_crawler_info.s(
                auth_token=auth_token,
                task_id=task_id,
                data_source='ptt',
                data_type=data['board_name'],
                is_multiple=is_multiple,
            ),
            task_id=task_id
        )()
    except Exception as e:
        logger.error(HandleException.show_exp_detail_message(e))
    return task_id

@shared_task(ignore_result=True)
def crawler_ptt_info(params, auth_user, task_id):
    logger.debug(params)
    final_result = {
        'task_mark': '',
        'json_rows': ''
    }
    try:
        ptt_info_obtain = PttInfoObtain(
            base_url=params['base_url'],
            board_name=params['board_name'],
            task_id=task_id,
            auth_user=auth_user
        )
        if params['action_mode'] == 'Page' and params['search_page_count'] > 0:
            final_result = ptt_info_obtain.ptt_scrape_by_page_count(search_page_count=params['search_page_count'])
            final_result['task_mark'] = f"{params['action_mode']},{params['search_page_count']}"
            del ptt_info_obtain
        elif params['action_mode'] == 'Keyword' and params['search_keyword'] is not None:
            if params['search_page_limit_enable'] is True:
                final_result = ptt_info_obtain.ptt_scrape_by_keyword(
                    keyword=params['search_keyword'],
                    search_page_limit=params['search_page_count'],
                    page_search_over_limit=False,
                )
                final_result['task_mark'] = f"{params['action_mode']},{params['search_keyword']},{params['search_page_count']}"
            else:
                final_result = ptt_info_obtain.ptt_scrape_by_keyword(
                    keyword=params['search_keyword'],
                    page_search_over_limit=True,
                )
                final_result['task_mark'] = f"{params['action_mode']},{params['search_keyword']},Max"
            del ptt_info_obtain
    except Exception as e:
        logger.error(HandleException.show_exp_detail_message(e))
    return final_result

@shared_task
def handle_crawler_info(result, **info):
    threading_result = []
    api_res_for_task = APIRequest(Init.api_endpoint['extra_task'])
    threading_result.append(
        api_res_for_task.postRequest(
            {
                'task': info['task_id'], 'data_source': info['data_source'],
                'data_type': info['data_type'], 'task_mark': result['task_mark'], 'is_multiple': info['is_multiple']
            },
            info['auth_token']
        )
    )
    api_res_for_save_info = APIRequest(Init.api_endpoint['ptt']['base'])

    if 'json_rows' in result and result['json_rows']:
        write_rows_count = len(result['json_rows'])
        logger.debug(f'rows total: {write_rows_count}')
        threading_result.append(
            api_res_for_save_info.postRequest(
            result['json_rows'],
            info['auth_token']
        ))
    # logger.debug(f"data: {result['json_rows']}")
    logger.debug(f"result: {threading_result}")
    if not result['json_rows'] or all(threading_result) is False:
        err_msg = f"Task {info['task_id']} run threading failed.\nResult: {threading_result}"
        raise Exception(err_msg)
    return threading_result