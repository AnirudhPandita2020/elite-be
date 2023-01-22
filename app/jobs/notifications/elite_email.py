import smtplib
import ssl
from email.message import EmailMessage
from typing import List

from app.utils.env_utils import setting

email_sender = setting.sender_email
email_receiver = setting.receiver_email
email_password = setting.email_password


async def send_email(truck_list: List):
    subject = f"Alert. Certification expiring of {len(truck_list)} trucks"
    body = f"""Greetings,
    
    Following trucks have their certificates expiring in less than 15 days.
    The details are mentioned below.
    
"""
    line_value = ""
    for trucks in truck_list:
        for data in trucks['data']:
            line_value += f"Trailer Number: {trucks['trailer_number']}\nValidity: {data['validity']}\nCertificate Type: {data['type']}\n\n"
    regards = "\nRegards,\n\nTruck & Trailer Management System\nElite Shipping Agencies India PVT LTD"
    print(body + line_value + regards)

    reminder_email = EmailMessage()
    reminder_email['From'] = email_sender
    reminder_email['To'] = email_receiver
    reminder_email['Subject'] = subject
    reminder_email.set_content(body + line_value + regards)

    context = ssl.create_default_context()

    smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context)
    smtp.login(email_sender, email_password)
    smtp.sendmail(email_sender, email_receiver, reminder_email.as_string())
