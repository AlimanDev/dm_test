from typing import List, Dict

import requests
from django.conf import settings
from requests.adapters import HTTPAdapter

from services.dashamail.schemas import DashaMailResponse


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

    def send(self) -> DashaMailResponse:
        """Отправляет рассылку по указанным почтовым адресам."""

        transport_adapter = HTTPAdapter(max_retries=3)
        session = requests.Session()
        session.mount(prefix=self.API, adapter=transport_adapter)

        try:
            response = session.post(url=self.API, params=self.get_params())
            result = response
        except requests.exceptions.ConnectionError as err_msg:
            result = str(err_msg)
        except requests.exceptions.Timeout as err_msg:
            result = str(err_msg)
        except requests.exceptions.RequestException as err_msg:
            result = str(err_msg)

        return DashaMailResponse(response=result)

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
