import os
import yaml
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# Get the path to the script directory
script_directory = os.path.dirname(__file__)

# Prepare the HTML content
current_timestamp = datetime.now().strftime('%Y-%m-%d')
subject = 'IMMUNIZE: OCI Images Patching Report'
html_body = f'<h1>Patched Images 💉 {current_timestamp}</h1><ul>'


html_body += '</ul><br />'
html_body += 'check the full catalog 📚 <a href="https://github.com/R3DRUN3?tab=packages&repo_name=immunize">here</a> !'
html_body += '<br /><br />'
html_body += '<h2>Stay Safe! 💪</h2>'

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
# Get all files named "*-openvex-report" in root of the project folder
report_files = [filename for filename in os.listdir(script_directory) if filename.endswith("-openvex-report")]
# Attach reports to the email
for report_file in report_files:
    html_body += f'<li>{report_file}</li>'
    with open(os.path.join(script_directory, report_file), 'rb') as file:
        part = MIMEApplication(file.read(), Name=os.path.basename(report_file))
        part['Content-Disposition'] = f'attachment; filename="{report_file}"'
        message.attach(part)

# Connect to the GMAIL SMTP server and send the emails
with smtplib.SMTP('smtp.gmail.com', 587) as server:
    server.starttls()
    server.login(email_address, email_password)
    server.sendmail(email_address, recipients, message.as_string())

print('Emails sent successfully!!')
