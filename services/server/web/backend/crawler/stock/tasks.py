from celery import shared_task, chain, uuid
from .background.stock_info_obtain import StockInfoObtain
from crawler.config import Initialization as Init
from module.log_generate import Loggings
from module.handle_exception import HandleException
from module.call_api import APIRequest
from threading import Thread
import queue


logger = Loggings()

def chain_tasks_run_stock_crawler(data, auth_token, auth_user, is_multiple):
    task_id = uuid()
    logger.info(f'Starting stock info crawler task id: {task_id}')
    try:
        chain(
            crawler_stock_info.s(
                params=data,
                auth_user=auth_user,
                task_id=task_id),
            handle_crawler_info.s(
                auth_token=auth_token,
                task_id=task_id,
                data_source='yahoo finance',
                is_multiple=is_multiple
            ),
            task_id=task_id
        )()
    except Exception as e:
        logger.error(HandleException.show_exp_detail_message(e))
    return task_id

@shared_task(ignore_result=True)
def crawler_stock_info(params, auth_user, task_id):
    threading_result = []
    que = queue.Queue()

    try:
        for val in params:
            job = []
            obj = StockInfoObtain(
                ticker=val['ticker'], country=val['country'],
                task_id=task_id, auth_user=auth_user,
            )
            logger.debug(f"Obtain stock ticker {val['ticker']} from {val['start_date']} to {val['end_date']}")
            job = Thread(target=lambda q, start, end: q.put(obj.obtain_history_records_v2(start, end)), args=(que,), kwargs=(
                {'start': f"{val['start_date']} 08:00:00", 'end': f"{val['end_date']} 23:59:59"}
            ))
            job.start()
            job.join()
            del obj

        task_mark = ''

        while not que.empty():
            temp_result = que.get()
            task_mark += temp_result['full_ticker'] + ','
            threading_result.extend(temp_result['json_rows'])
        task_mark = task_mark.strip(',')

        logger.info(f'stock info catch data count: {len(threading_result)}')
        final_result = {'json_rows': threading_result, 'full_ticker': task_mark}
        # logger.info(f'{final_result}')
    except Exception as e:
        logger.error(HandleException.show_exp_detail_message(e))
    return final_result

@shared_task
def handle_crawler_info(result, data_source, auth_token, task_id, is_multiple):
    threading_result = []
    api_res_for_task = APIRequest(Init.api_endpoint['extra_task'])
    threading_result.append(
        api_res_for_task.postRequest(
            {
                'task': task_id, 'data_source': data_source,
                'data_type': 'stock', 'task_mark': result['full_ticker'], 'is_multiple': is_multiple
            },
            auth_token
        )
    )
    api_res_for_save_info = APIRequest(Init.api_endpoint['stock']['base'])

    if 'json_rows' in result and result['json_rows']:
        write_rows_count = len(result['json_rows'])
        logger.debug(f'rows total: {write_rows_count}')
        threading_result.append(
            api_res_for_save_info.postRequest(
            result['json_rows'],
            auth_token
        ))
    if not result['json_rows'] or all(threading_result) is False:
        err_msg = f"Task {task_id} run threading failed.\nResult: {threading_result}"
        raise Exception(err_msg)
    return threading_result