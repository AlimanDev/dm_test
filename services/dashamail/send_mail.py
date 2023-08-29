from typing import List, Dict

import requests
from django.conf import settings
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from services.dashamail.exceptions import DashaMailTransactionException


class DashaMailTransaction:
    API = 'https://api.dashamail.com/'
    API_KEY = settings.DASHAMAIL_API_KEY
    FROM_EMAIL = settings.DASHAMAIL_FROM_EMAIL
    METHOD = 'transactional.send'

    emails: List[str]
    mailing_id: str

    def __init__(self, emails: List[str], mailing_id: str):
        """
        :param emails: почтовые адреса.
        :param mailing_id: ID шаблона рассылки.
        """

        self.emails = emails
        self.mailing_id = mailing_id

    def send(self) -> dict[str, str]:
        """Отправляет рассылку по указанным почтовым адресам."""

        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["POST"],
            backoff_factor=1
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session = requests.Session()
        session.mount("https://", adapter)

        try:
            response = session.post(url=self.API, params=self.get_params())
            print(f'status_code: {response.status_code}')
            response.raise_for_status()
            data = response.json()
            response_type = data['response']['msg']['type']
            if response_type == 'message':
                transaction_id = data['response']['data']['transaction_id']
                return {'transaction_id': transaction_id}
            else:
                raise DashaMailTransactionException(data['response']['msg']['text'])
        except (requests.exceptions.RequestException, requests.exceptions.JSONDecodeError, KeyError) as e:
            raise DashaMailTransactionException(e)
            # return response

    def get_params(self) -> Dict[str, str]:
        """Формирует параметры запроса рассылки."""

        params = {
            'method': self.METHOD,
            'api_key': self.API_KEY,
            'to': ','.join(self.emails),
            'from_email': self.FROM_EMAIL,
            'message': self.mailing_id,
        }
        return params
