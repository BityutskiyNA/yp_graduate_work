import datetime

from .src.databases.db import pg_create
from .src.services.sender_message import send_email
from .src.services.sender_rabit import send_to_qulle


class Message:
    def __init__(self, data):
        self.mailing_data = data

    def message_validation(self):
        if self.mailing_data.events_name == 'new':
            result = True
        elif self.mailing_data.events_name == 'like':
            result = True
        else:
            result = True
        return result

    def time_zone_checking(self):
        min6 = datetime.timezone(datetime.timedelta(hours=self.mailing_data.time_zone))
        d = datetime.datetime.now(min6).time()
        t1 = datetime.time(9, 00)
        t2 = datetime.time(21, 00)

        return t1 < d < t2

    def to_json(self):
        return self.mailing_data.to_json

    def database_status(self, status):
        pg_create(self.to_json(), status)

    def send_message(self):
        self.database_status('Message create')

        if self.mailing_data.time_zone_check and not self.time_zone_checking():
            self.database_status('message sent to the pending message queue')
            send_to_qulle(self.to_json(), "queue_for_postponed_messages")
            return None

        if self.mailing_data.validation and not self.message_validation():
            self.database_status('Message deleted as not relevant')
            return None
        self.database_status('Message sending')
        try:
            if self.mailing_data.agent == 'mail':
                send_email(self)
                self.database_status('Message send')
        except:
            send_to_qulle(self.to_json(), "queue_for_error_messages")
            self.database_status('Message error')
