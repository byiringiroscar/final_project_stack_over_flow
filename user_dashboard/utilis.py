from django.core.mail import EmailMessage
from django.template.loader import get_template
import threading


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)


class Util:
    @staticmethod
    def send_email(subject, html_content, from_email, email):
        email = EmailMessage(subject, html_content, from_email, to=[email, ])
        email.send()
