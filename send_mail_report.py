import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import yaml
#import html
from datetime import datetime

# Get the path to the YAML file
yaml_file_path = os.path.join(os.path.dirname(__file__), '.github/workflows/patch.yaml')

# Read the YAML file to get the patched image list
with open(yaml_file_path, 'r') as yaml_file:
    yaml_content = yaml.load(yaml_file, Loader=yaml.FullLoader)
    patched_images = yaml_content.get('jobs', {}).get('immunize', {}).get('strategy', {}).get('matrix', {}).get('images', [])

print("Patched images:", patched_images)
# Get the current timestamp
current_timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
# Prepare the HTML content
subject = 'IMMUNIZE: Patched Image Report'
html_body = '<h2>Patched Images 💉- {}</h2><ul>'.format(current_timestamp)
for image in patched_images:
    # encoded_image_name = html.escape(image)
    github_link = f'https://github.com/r3drun3/pkgs/container/immunize/{image}'
    html_body += f'<li>{image}</li>'
html_body += '</ul><br />'
html_body += 'check the full catalog <a href="https://github.com/R3DRUN3?tab=packages&repo_name=immunize">here</a>'

# Get email and password from GitHub secrets
email_address = os.environ.get('EMAIL_ADDRESS', '')
email_password = os.environ.get('EMAIL_PASSWORD', '')

# Get email recipients from GitHub secret
recipients = os.environ.get('EMAIL_RECIPIENTS', '').split(',')

# Prepare the email message
message = MIMEMultipart()
message['From'] = email_address
message['To'] = ', '.join(recipients)
message['Subject'] = subject
message.attach(MIMEText(html_body, 'html'))

# Connect to the GMAIL SMTP server and send the emails
with smtplib.SMTP('smtp.gmail.com', 587) as server:
    server.starttls()
    server.login(email_address, email_password)
    server.sendmail(email_address, recipients, message.as_string())

print('Email sent successfully!')
