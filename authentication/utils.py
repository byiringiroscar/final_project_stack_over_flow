from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
import requests


def send_sms(user_code, phone_number):
    data = {
        'recipients': f'{phone_number}',
        'message': f'Confirm this Pin in order to login - {user_code}',
        'sender': '+250786405263',
    }

    r = requests.post('https://www.intouchsms.co.rw/api/sendsms/.json', data,
                      auth=('byiringoroscar@gmail.com', 'oscarlewis.O1'))
    # print(r.json(), r.status_code)

class AppTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (text_type(user.is_verified) + text_type(user.pk) + text_type(timestamp))


account_activation_token = AppTokenGenerator()
