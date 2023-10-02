from datetime import date

import pytest

from mailing.models import Mailing_type, Mail_account, Mailing_list, Mailing_data, System_events


@pytest.fixture
@pytest.mark.django_db
def mailing_type(client):
    mailing_type = Mailing_type.objects.create(
        name='test',
        agent='mail',
        mail_template='templates/mail.html',
        time_control=False,
        data_control=False
    )
    return mailing_type


@pytest.fixture
@pytest.mark.django_db
def mail_account(client):
    mail_account = Mail_account.objects.create(
        name='test',
        login='test',
        password='test',
        domain='test',
        smtp_host='test',
        smtp_port='test',
        sender='test',
        api_key='test',
        created=date.today()
    )
    return mail_account


@pytest.fixture
@pytest.mark.django_db
def mailing_list(client, mail_account, mailing_type):
    mailing_list = Mailing_list.objects.create(
        name='test',
        subject='test',
        mailing_type=mailing_type,
        primary=True,
        urgent=False,
        sent_out=False,
        created=False,
        day_send='0',
        dispatch_time_hour=15,
        send_time_minute=30,
        single_mailing=True,
        mail_account=mail_account,
    )
    return mailing_list


@pytest.fixture
@pytest.mark.django_db
def mailing_data(client, mailing_list):
    mailing_data = Mailing_data.objects.create(
        name='test',
        value='test',
        mail_data=mailing_list,
        created=date.today(),
    )
    return mailing_data

@pytest.fixture
@pytest.mark.django_db
def system_events(client, mailing_type):
    system_event = System_events.objects.create(
        events_name='test',
        mailing_type=mailing_type,
    )
    return system_event


@pytest.fixture
@pytest.mark.django_db
def html_content(client, mailing_type):
    html_content_bytes = mailing_type.mail_template.read()
    html_content = html_content_bytes.decode('utf-8')
    return html_content
