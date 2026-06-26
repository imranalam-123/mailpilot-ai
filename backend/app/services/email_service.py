import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.core.config import (
    EMAIL_ADDRESS,
    EMAIL_PASSWORD
)


def send_email(to_email: str, subject: str, body: str):

    try:
        print("Connecting to Gmail...")

        message = MIMEMultipart()

        message["From"] = EMAIL_ADDRESS
        message["To"] = to_email
        message["Subject"] = subject

        message.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        print("Logging in...")
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        print("Sending email...")
        server.sendmail(
            EMAIL_ADDRESS,
            to_email,
            message.as_string()
        )

        server.quit()

        print("SUCCESS")

        return {
            "message": "Email Sent Successfully"
        }

    except Exception as e:
        print("ERROR:", e)

        return {
            "error": str(e)
        }