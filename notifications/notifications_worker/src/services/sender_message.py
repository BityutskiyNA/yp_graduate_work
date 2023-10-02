import jinja2
import requests

from notifications.notifications_admin.config import app_settings


def send_email(mail):
    api_key = mail.mailing_data.api_key
    sender = mail.mailing_data.sender

    mailgun_url = app_settings.mailgun_url

    auth = ("api", api_key)
    data = {
        "from": sender,
        "to":  mail.mailing_data.email,
        "subject":  mail.mailing_data.Subject,
        "text": "test",
    }
    if mail.template:
        template_content = mail.template
        template = jinja2.Template(template_content)
        rendered_html = template.render(subject=mail.Subject, heading=mail.mailing_data.data.title, message=mail.mailing_data.data.text)
        data["html"] = rendered_html

    response = requests.post(mailgun_url,auth=auth, data=data)
    response.raise_for_status()

    if response.status_code == 200:
        return True


