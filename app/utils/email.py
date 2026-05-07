import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
DEFAULT_SENDER = os.environ.get(
    "MAIL_DEFAULT_SENDER",
    "ChargeMate <ev.services.chargemate@gmail.com>"
)

def send_email(to, subject, body):
    try:
        message = Mail(
            from_email=DEFAULT_SENDER,
            to_emails=to,
            subject=subject,
            html_content=body
        )

        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)

        return response.status_code in [200, 202]

    except Exception as e:
        print("SENDGRID ERROR:", e)
        return False
