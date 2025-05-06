import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os

# Load env vars
load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_email(subject, content, recipient_email):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = recipient_email
    msg.set_content(content)
    print(EMAIL_ADDRESS)
    print(EMAIL_PASSWORD)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print(f"✅ Email sent to {recipient_email}")
    except Exception as e:
        print("❌ Error sending email:", e)
