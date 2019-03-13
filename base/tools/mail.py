from flask_mail import Mail, Message
from flask import current_app as app
import logging
log = logging.getLogger(__name__)

def send_email(subject, sender, recipients, text_body, html_body=None):
    '''Actually send email to recipient'''

    mail = Mail(app)
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body

    if not app.config['NOMAIL']:
        mail.send(msg)
    else:
        logging.info(msg.body)
