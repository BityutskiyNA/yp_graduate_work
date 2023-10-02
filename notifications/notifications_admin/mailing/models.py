from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class MailingType(models.Model):
    agent_list = [
        ("mail", "mail"),
        ("web_push", "web_push"),
        ("sms", "sms"),
        ("messenger", "messenger"),
    ]
    name = models.CharField(max_length=200)
    mail_template = models.FileField(upload_to='templates', default='')
    agent = models.CharField(max_length=10, choices=agent_list)
    time_control = models.BooleanField(default=True)
    data_control = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class MailAccount(models.Model):
    name = models.CharField(max_length=50)
    login = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    domain = models.CharField(max_length=50)
    smtp_host = models.CharField(max_length=50)
    smtp_port = models.CharField(max_length=4)
    sender = models.CharField(max_length=200)
    api_key = models.CharField(max_length=50)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class MailingList(models.Model):
    data_day = [
        ("0", "Monday"),
        ("1", "Tuesday"),
        ("2", "Wednesday"),
        ("3", "Thursday"),
        ("4", "Friday"),
        ("5", "Saturday"),
        ("6", "Sunday"),
    ]
    name = models.CharField(max_length=200)
    subject = models.CharField(max_length=500)
    mailing_type = models.ForeignKey(MailingType, on_delete=models.CASCADE)
    primary = models.BooleanField(default=False)
    urgent = models.BooleanField(default=False)
    sent_out = models.BooleanField(default=False)
    last_sent_time = models.DateField(null=True)
    created = models.DateField(auto_now_add=True)
    day_send = models.CharField(max_length=10, choices=data_day, default="monday")
    dispatch_time_hour = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(23)
        ])
    send_time_minute = models.IntegerField(validators=[
        MinValueValidator(0),
        MaxValueValidator(59)
    ])
    single_mailing = models.BooleanField(default=False)
    mail_account = models.ForeignKey(MailAccount, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class MailingData(models.Model):
    data_name = [
        ("title", "title"),
        ("text", "text"),
        ("image", "image"),
    ]
    name = models.CharField(max_length=50, choices=data_name)
    value = models.CharField(max_length=2000)
    mail_data = models.ForeignKey(MailingList, on_delete=models.DO_NOTHING)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class SystemEvents(models.Model):
    events_name = models.CharField(max_length=200)
    mailing_type = models.ForeignKey(MailingType, on_delete=models.CASCADE)

    def __str__(self):
        return self.events_name


class Messengers(models.Model):
    name = models.CharField(max_length=50)
    api_token = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class MessengerList(models.Model):
    name = models.CharField(max_length=50)
    messenger = models.ForeignKey(Messengers, on_delete=models.DO_NOTHING)
    mailing_type = models.ForeignKey(MailingType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class PushServices(models.Model):
    name = models.CharField(max_length=50)
    api_token = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class WebPushList(models.Model):
    name = models.CharField(max_length=50)
    push_services = models.ForeignKey(PushServices, on_delete=models.DO_NOTHING)
    mailing_type = models.ForeignKey(MailingType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
class SmsOperators(models.Model):
    name = models.CharField(max_length=50)
    api_token = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class SmsList(models.Model):
    name = models.CharField(max_length=50)
    sms_operator = models.ForeignKey(SmsOperators, on_delete=models.DO_NOTHING)
    mailing_type = models.ForeignKey(MailingType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name