import pytest
from datetime import date

from mailing.models import Mailing_list


@pytest.mark.django_db
def test_mailing_type_view_empty(client, mailing_type, mail_account, mailing_list, mailing_data, html_content,
                                 system_events):
    expected_response = []

    response = client.post("/mailing/planet_mailing/")
    assert response.status_code == 200
    assert expected_response == response.json()


@pytest.mark.django_db
def test_mailing_type_view(client, mailing_type, mail_account, mailing_data, html_content, system_events):
    mailing_list = Mailing_list.objects.create(
        name='test',
        subject='test',
        mailing_type=mailing_type,
        primary=True,
        urgent=False,
        sent_out=False,
        created=False,
        day_send=date.today().weekday(),
        dispatch_time_hour=0,
        send_time_minute=0,
        single_mailing=True,
        mail_account=mail_account,
    )

    expected_response = {
        'mailing_type': mailing_type.pk,
        'mailing_type_agent': mailing_type.agent,
        'validation': mailing_type.data_control,
        'time_zone_check': mailing_type.time_control,
        'login': mail_account.login,
        'password': mail_account.password,
        'domain': mail_account.domain,
        'smtp_host': mail_account.smtp_host,
        'smtp_port': mail_account.smtp_port,
        'subject': mailing_list.subject,
        'template': html_content,
        'data': {}
    }
    expected_response_list = list()
    expected_response_list.append(expected_response)

    response = client.post("/mailing/planet_mailing/")
    assert response.status_code == 200
    assert expected_response_list == response.json()


@pytest.mark.django_db
def test_mailing_type_view_invalid_query(client, mailing_type, mail_account, mailing_list, mailing_data, html_content,
                                         system_events):

    response = client.get("/mailing/planet_mailing/")
    assert response.status_code == 405
