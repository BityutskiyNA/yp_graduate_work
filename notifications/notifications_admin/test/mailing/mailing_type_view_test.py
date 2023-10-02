import pytest


@pytest.mark.django_db
def test_mailing_type_view(client, mailing_type, mail_account, mailing_list, mailing_data, html_content):
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
        'data': {
            mailing_data.name: mailing_data.value
        }
    }

    response = client.get(f"/mailing/mailing_type/{mailing_type.pk}/")
    assert response.status_code == 200
    assert expected_response == response.json()


@pytest.mark.django_db
def test_mailing_type_view_invalid_query(client, mailing_type):
    response = client.post(f"/mailing/mailing_type/{mailing_type.pk}/")
    assert response.status_code == 305
