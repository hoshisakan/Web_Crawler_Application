from celery import shared_task, chain, uuid
from crawler.config import Initialization as Init
from module.log_generate import Loggings
from module.handle_exception import HandleException
# from module.handle_file import FileOperation
# from threading import Thread
# import queue
from module.call_api import APIRequest
# import os

logger = Loggings()
# file_operation = FileOperation(path=os.getcwd())


def chain_tasks_run_remove_info(**task):
    task_id = uuid()
    try:
        logger.info(f'Starting execute remove info of task id: {task_id}')
        chain(remove_specific_task_all_info.s(
            remove_task_id=task['remove_task_id'],
            # task_status=task['task_status'],
            data_type=task['data_type'], auth_token=task['auth_token'],
            data_source=task['data_source']
            ),task_id=task_id)()
    except Exception as e:
        logger.error(HandleException.show_exp_detail_message(e))
    return task_id

@shared_task(ignore_result=True)
def remove_specific_task_all_info(**task):
    data_clear_api_endpoint = None
    threading_result = []

    if task['data_source'] == 'google search' and task['data_type'] in ['google news', 'google video', 'google shopping']:
        data_clear_api_endpoint = Init.api_endpoint['google_search'][task['data_type']]['extra']
    elif task['data_source'] == 'yahoo finance':
        data_clear_api_endpoint = Init.api_endpoint['stock']['extra']
    elif task['data_source'] in ['cpbl']:
        data_clear_api_endpoint = Init.api_endpoint['baseball'][task['data_source']]['extra']
    elif task['data_source'] == 'ptt':
        data_clear_api_endpoint = Init.api_endpoint['ptt']['extra']
    else:
        raise Exception("Unknown data type.")

    api_res_for_data_clear = APIRequest(data_clear_api_endpoint)
    logger.info(f"Will be remove task {task['remove_task_id']} that data type is: {task['data_type']}")
    # logger.info(f"Will be remove task {task['remove_task_id']} that task execute status is: {task['task_status']} and data type is: {task['data_type']}")
    threading_result = api_res_for_data_clear.deleteRequestByPayload({'task_id': task['remove_task_id']}, task['auth_token'])

    if not threading_result or threading_result is False:
        err_msg = f"Task {task['remove_task_id']} run threading failed.\nResult: {threading_result}"
        logger.error(err_msg)
        raise Exception(err_msg)
    return threading_result
