# SEND MAIL REPORT WITH PATCHED IMAGES

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Get patched image information from GitHub Actions context
patched_images_str = os.environ.get('PATCHED_IMAGES', '')
print("Pathed images string: ", patched_images_str)
patched_images = patched_images_str.split(',')
print("Pathed images: ", patched_images)

# Prepare the email content
subject = 'Patched Image Report'
body = f'Patched Images:\n\n{", ".join(patched_images)}'

# Get email and password from GitHub secrets
email_address = os.environ.get('EMAIL_ADDRESS', '')
print("Email address:", email_address)
email_password = os.environ.get('EMAIL_PASSWORD', '')

# Get email recipients from GitHub secret
recipients = os.environ.get('EMAIL_RECIPIENTS', '').split(',')
print("Recipients:", recipients)

# Prepare the email message
message = MIMEMultipart()
message['From'] = email_address
message['To'] = ', '.join(recipients)
message['Subject'] = subject
message.attach(MIMEText(body, 'plain'))

# Connect to the SMTP server and send the email
with smtplib.SMTP('smtp.gmail.com', 587) as server:
    server.starttls()
    server.login(email_address, email_password)
    server.send_message(message)

print('Email sent successfully!')
