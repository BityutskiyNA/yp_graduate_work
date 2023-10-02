from datetime import timedelta
from django.utils import timezone

from mailing.models import MailingList, MailingType, MailingData
from django.db.models import Q


def process_message(current_time, data_messages, message, is_periodic=False):
    if (is_periodic and (message.last_sent_time is None or (current_time - message.last_sent_time) >= timedelta(
            days=7))) or not is_periodic:
        mail_account = message.mail_account
        data_list = list(MailingData.objects.filter(mail_data=message.pk).values('name', 'value'))
        data = {item['name']: item['value'] for item in data_list}
        mailing_type = MailingType.objects.filter(id=message.mailing_type_id).first()
        html_content_bytes = mailing_type.mail_template.read()
        html_content = html_content_bytes.decode('utf-8')
        message_data = {
            'mailing_type': mailing_type.pk,
            'mailing_type_agent': mailing_type.agent,
            'validation': mailing_type.data_control,
            'time_zone_check': mailing_type.time_control,
            'login': mail_account.login,
            'password': mail_account.password,
            'domain': mail_account.domain,
            'smtp_host': mail_account.smtp_host,
            'smtp_port': mail_account.smtp_port,
            'subject': message.subject,
            'template': html_content,
            'data': data
        }
        data_messages.append(message_data)
        message.sent_out = True
        if is_periodic:
            message.last_sent_time = current_time
        message.save()
    return data_messages


def send_scheduled_mailings():
    current_time = timezone.now()
    messages_to_send = MailingList.objects.filter(Q(single_mailing=False) | Q(sent_out=False))
    one_time_messages = messages_to_send.filter(single_mailing=False)
    periodic_messages = messages_to_send.filter(single_mailing=True, day_send=current_time.weekday(),
                                                dispatch_time_hour__lt=current_time.hour,
                                                send_time_minute__lt=current_time.minute)
    data_messages = []

    for message in one_time_messages:
        data_messages = process_message(current_time, data_messages, message)

    for message in periodic_messages:
        data_messages = process_message(current_time, data_messages, message, is_periodic=True)

    return data_messages
