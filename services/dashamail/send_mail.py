import requests
from django.conf import settings

from services.dashamail.schemas import DashaMailResponse


class DashaMail:
    API = 'https://api.dashamail.com/'

    @staticmethod
    def get_params_newsletter(emails: list, mailing_id: str) -> dict:
        """Формирует параметры запроса рассылки."""

        params = {
            'method': 'transactional.send',
            'api_key': settings.DASHAMAIL_API_KEY,
            'to': ','.join(emails),
            'from_email': settings.DASHAMAIL_FROM_EMAIL,
            'message': settings.DASHAMAIL_MAILING_ID,
        }
        return params

    def send_newsletter(self, emails: list, mailing_id: str) -> requests:
        """
        Отправляет рассылку по указанным почтовым адресам.
        :param emails: почтовые адреса.
        :param mailing_id: ID шаблона рассылки.
        :return: результат запроса.
        """

        params = self.get_params_newsletter(emails=emails, mailing_id=mailing_id)
        response = requests.post(url=self.API, params=params)
        return DashaMailResponse(result=response)
