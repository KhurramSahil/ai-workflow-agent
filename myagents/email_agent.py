import json
import smtplib
from email.mime.text import MIMEText


def load_config():
    with open('config/config.json', 'r') as f:
        return json.load(f)

config = load_config()

class EmailAgent:
    def send_notification(self, subject, body):
        """Send email notification"""
        try:
            msg = MIMEText(body, "plain")
            msg["Subject"] = subject
            msg["From"] = config['email']['sender_email']
            msg["To"] = config['email']['receiver_email']

            with smtplib.SMTP(config['email']['smtp_server'], config['email']['smtp_port']) as server:
                server.starttls()
                server.login(config['email']['username'], config['email']['password'])
                server.sendmail(
                    config['email']['sender_email'],
                    config['email']['receiver_email'],
                    msg.as_string()
                )
            return True
        except Exception as e:
            print(f"Email error: {e}")
            return False