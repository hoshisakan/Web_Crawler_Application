from celery import shared_task, chain, uuid
from module.log_generate import Loggings
from module.handle_exception import HandleException
from .send import send_email

logger = Loggings()

def chain_tasks_send_email(**mail):
    task_id = uuid()
    try:
        logger.info(f'Initialztion starting task id: {task_id}')
        chain(send_email_to_user.s(
            task_id=task_id,
            subject=mail['subject'],
            to=mail['to'],
            template=mail['template'],
            link=mail['link'],
            username=mail['username'],
        ), task_id=task_id)()
    except Exception as e:
        logger.error(HandleException.show_exp_detail_message(e))
    return task_id

@shared_task(ignore_result=True)
def send_email_to_user(**mail):
    mail_sent_result = send_email(
      subject=mail['subject'],
      to=mail['to'],
      template=mail['template'],
      link=mail['link'],
      username=mail['username'],
    )
    logger.info(f"The task {mail['task_id']} send email result: {mail_sent_result}")
    return mail_sent_result