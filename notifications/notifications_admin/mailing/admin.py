from django.contrib import admin
from django.utils.html import format_html

from mailing.models import MailingType, MailingList, SystemEvents, MailAccount, MailingData, SmsList, SmsOperators, \
    WebPushList, PushServices, Messengers

from notifications.notifications_admin.mailing.models import MessengerList


class Mailing_dataAdmin(admin.TabularInline):
    model = MailingData
    extra = 1


@admin.register(MailingList)
class Mailing_listAdmin(admin.ModelAdmin):
    inlines = [Mailing_dataAdmin]
    list_display = ('name', 'mailing_type', 'primary', 'urgent', 'sent_out', 'created', 'send_button')
    search_fields = ('name',)
    list_filter = ('name',)

    def send_button(self, obj):
        process_url = f"/mailing/process_mailing/{obj.pk}/"
        button_html = '<a class="button" href="{}"><img src="/path/to/process_icon.png" alt="Sell" /></a>'.format(
            process_url)
        return format_html(button_html)

    send_button.short_description = ''
    send_button.allow_tags = True


admin.site.register(MailingType)
admin.site.register(SystemEvents)
admin.site.register(MailAccount)
admin.site.register(SystemEvents)
admin.site.register(Messengers)
admin.site.register(MessengerList)
admin.site.register(PushServices)
admin.site.register(WebPushList)
admin.site.register(SmsOperators)
admin.site.register(SmsList)