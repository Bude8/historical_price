import os
import smtplib
from email.message import EmailMessage

EMAIL_ADDRESS = os.environ.get("EMAIL_USER")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

msg = EmailMessage()
msg['From'] = EMAIL_ADDRESS
msg['To'] = "price.tracker.1337@gmail.com"
msg['Subject'] = "Grab dinner this weekend?"
msg.set_content("How about dinner at 6pm this Saturday?")

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    smtp.send_message(msg)

# Debug
# with smtplib.SMTP("localhost", 1025) as smtp:  # to debug, run $ python3 -m smtpd -c DebuggingServer -n localhost:1025
