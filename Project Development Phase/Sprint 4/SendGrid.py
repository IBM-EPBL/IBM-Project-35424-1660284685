import sendgrid
import os
from sendgrid.helpers.mail import *

sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
from_email = Email("92172019104101@smartinternz.com")
to_email = To("92172019104101@smartinternz.com")
subject = "Sending with SendGrid"
content = Content("text/plain", "SendGrid Integrated With Python Successfully!")
mail = Mail(from_email, to_email, subject, content)
response = sg.client.mail.send.post(request_body=mail.get())
print(response.status_code)
print(response.body)
print(response.headers)

