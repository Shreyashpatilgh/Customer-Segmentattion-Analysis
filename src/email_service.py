import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_otp_email(receiver_email, otp):

    sender_email = os.getenv("SMTP_EMAIL")
    app_password = os.getenv("SMTP_APP_PASSWORD")

    if not sender_email or not app_password:
        raise RuntimeError(
            "Set SMTP_EMAIL and SMTP_APP_PASSWORD before sending OTP emails."
        )

    subject = "Airlines Analytics OTP Verification"

    body = f"""
Hello,

Your OTP verification code is:

{otp}

Please enter this OTP to verify your account.

Thank You
Airlines Analytics Suite
"""

    msg = MIMEMultipart()

    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP("smtp.gmail.com", 587)

    server.starttls()

    server.login(sender_email, app_password)

    server.send_message(msg)

    server.quit()
