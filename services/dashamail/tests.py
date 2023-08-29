import unittest
from unittest.mock import patch

import requests
from requests import Session

from services.dashamail.exceptions import DashaMailTransactionException
from services.dashamail.send_mail import DashaMailTransaction


class TestDashaMailTransaction(unittest.TestCase):

    def setUp(self) -> None:
        super(TestDashaMailTransaction, self).setUp()
        emails = ['alimandeveloper@gmail.com']
        mailing_id = 'mailing_id_123'
        self.dasha_mail = DashaMailTransaction(emails=emails, mailing_id=mailing_id)

    @patch.object(Session, 'post')
    def test_send_success(self, mock_post):
        transaction_id = {'transaction_id': 'unique_1'}
        fake_result_success = {
            'response': {
                'msg': {'err_code': 0, 'text': '', 'type': 'message'},
                'data': transaction_id
            }
        }
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = fake_result_success

        self.assertEquals(self.dasha_mail.send(), transaction_id)

    @patch.object(Session, 'post')
    def test_send_error(self, mock_post):
        fake_result_error = {
            'response': {
                'msg': {'err_code': 1, 'text': 'Неверный логин и(или) пароль', 'type': 'error'},
                # 'msg': {'err_code': 6, 'text': 'Некорректный email-адрес', 'type': 'error'},
                # 'msg': {'err_code': 999, 'text': 'Неизвестный метод', 'type': 'error'},
                'data': None
            }
        }
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = fake_result_error

        self.assertRaises(DashaMailTransactionException, self.dasha_mail.send)

    @patch.object(Session, 'post')
    def test_send_raise(self, mock_post):
        for exception in (requests.exceptions.RequestException, requests.exceptions.InvalidJSONError, KeyError):
            mock_post.return_value.raise_for_status.side_effect = exception
            self.assertRaises(DashaMailTransactionException, self.dasha_mail.send)
