from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView

from mailing.models import MailingList, MailingType, MailingData, SystemEvents
from mailing.servises import send_data_to_fastapi
from mailing.tasks import send_scheduled_mailings


def process_mailing(request, pk):
    mailing_list = get_object_or_404(MailingList, pk=pk)
    mailing_type = MailingType.objects.filter(id=mailing_list.mailing_type_id)
    mail_account = mailing_list.mail_account
    data_list = list(MailingData.objects.filter(mail_data=mailing_list.pk).values('name', 'value'))
    data = {item['name']: item['value'] for item in data_list}
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
        'subject': mailing_list.subject,
        'template': html_content,
        'data': data
    }
    send_data_to_fastapi(message_data)

    return redirect('admin:mailing_mailing_list_changelist')


@method_decorator(csrf_exempt, name='dispatch')
class MailingTypeView(DetailView):
    model = MailingType

    def get(self, request, *args, **kwargs):
        mailing_type = self.get_object()
        mailing_list = MailingList.objects.get(mailing_type=mailing_type, primary=True)
        mail_account = mailing_list.mail_account
        data_list = list(MailingData.objects.filter(mail_data=mailing_list.pk).values('name', 'value'))
        data = {item['name']: item['value'] for item in data_list}
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
            'subject': mailing_list.subject,
            'template': html_content,
            'data': data
        }
        return JsonResponse(message_data, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class SystemEventsView(View):
    def get(self, request, *args, **kwargs):
        system_events_name = kwargs['name']
        system_events = SystemEvents.objects.filter(events_name=system_events_name).values('mailing_type_id').first()
        mailing_type = MailingType.objects.get(id=system_events['mailing_type_id'])
        mailing_list = MailingList.objects.get(mailing_type=mailing_type.pk, primary=True)
        mail_account = mailing_list.mail_account
        data_list = list(MailingData.objects.filter(mail_data=mailing_list.pk).values('name', 'value'))
        data = {item['name']: item['value'] for item in data_list}
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
            'subject': mailing_list.subject,
            'template': html_content,
            'data': data
        }
        return JsonResponse(message_data, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class PlannedMailingView(View):
    def post(self, request, *args, **kwargs):
        message_data = send_scheduled_mailings()
        return JsonResponse(message_data, safe=False)
