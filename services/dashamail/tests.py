import pytest
from django.conf import settings

from services.dashamail.send_mail import DashaMail

dashamail = DashaMail()


@pytest.mark.parametrize(
    "emails", [
        ['alimandeveloper@gmail.com'],
        ['alimandeveloper@gmail.com', 'fsdamp@gmail.com'],
        ['alimandeveloper@gmail.com', 'fsdamp@gmail.com', 'fsdamp.job@gmail.com'],
    ]
)
def test_params_newsletter(emails):
    params = {
        'method': 'transactional.send',
        'api_key': settings.DASHAMAIL_API_KEY,
        'to': ','.join(emails),
        'from_email': settings.DASHAMAIL_FROM_EMAIL,
        'message': settings.DASHAMAIL_MAILING_ID,
    }

    assert dashamail.get_params_newsletter(
        emails=emails, mailing_id=settings.DASHAMAIL_MAILING_ID
    ) == params


@pytest.mark.parametrize(
    "emails", [
        ['alimandeveloper@gmail.com'],
        ['alimandeveloper@gmail.com', 'fsdamp@gmail.com'],
        ['alimandeveloper@gmail.com', 'fsdamp@gmail.com', 'fsdamp.job@gmail.com'],
    ]
)
def test_send_newsletter(emails):
    response = dashamail.send_newsletter(
        emails=emails, mailing_id=settings.DASHAMAIL_MAILING_ID
    )
    assert response.status_code == 200 and response.err_code == 0
