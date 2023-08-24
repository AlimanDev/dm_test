import unittest
from unittest.mock import patch

from services.dashamail.send_mail import DashaMailTransaction


class TestDashaMailTransaction(unittest.TestCase):

    def test_send(self):
        fake_result = {
            'http_status_code': 200,
            'error_code': -1000,
            'error_message': 'Error Connection'
        }

        with patch('services.dashamail.send_mail.DashaMailTransaction.send') as mock_get:
            mock_get.return_value.http_status_code = 200
            mock_get.return_value.__dict__ = fake_result

            emails = ['alimandeveloper@gmail.com']
            mailing_id = 'mailing_id_123'
            dasha_mail = DashaMailTransaction(emails=emails, mailing_id=mailing_id)
            response = dasha_mail.send()

        self.assertEquals(response.http_status_code, 200)
        self.assertEquals(response.__dict__, fake_result)
