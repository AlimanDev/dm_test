import unittest
from unittest.mock import patch

from services.dashamail.send_mail import DashaMailTransaction, DashaMailTransactionException


class TestDashaMailTransaction(unittest.TestCase):

    def setUp(self) -> None:
        super(TestDashaMailTransaction, self).setUp()
        self.emails = ['alimandeveloper@gmail.com']
        self.mailing_id = 'mailing_id_123'

    def test_send_success(self):

        fake_result_success = {'transaction_id': 'transaction_1'}

        with patch('services.dashamail.send_mail.DashaMailTransaction.send') as mock_get:
            mock_get.return_value = fake_result_success
            dasha_mail = DashaMailTransaction(emails=self.emails, mailing_id=self.mailing_id)
            response = dasha_mail.send()

        self.assertEquals(response, fake_result_success)

    def test_send_raise(self):

        with patch('services.dashamail.send_mail.DashaMailTransaction.send') as mock_get:
            mock_get.return_value = DashaMailTransaction
            dasha_mail = DashaMailTransaction(emails=self.emails, mailing_id=self.mailing_id)

        self.assertRaises(DashaMailTransactionException, dasha_mail.send)
