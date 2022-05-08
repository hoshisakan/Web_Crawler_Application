# from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string

def send_email(**mail):
    subject = mail['subject']
    to = mail['to']
    html_content = render_to_string(mail['template'], {
        'link': mail['link'],
        'username': mail['username'],
    })
    email = EmailMultiAlternatives(
            subject=subject,
            from_email=settings.EMAIL_HOST_USER,
            to=to)
    email.attach_alternative(html_content, 'text/html')
    return email.send()