import json
import os
import requests


sender_email = os.getenv("MY_SENDER_EMAIL")
api_key = os.getenv('SENDGRID_API_KEY')


def send_email_to_one_recipient(recipient_email, subject, message):
    if sender_email and api_key and recipient_email:
        url = "https://api.sendgrid.com/v3/mail/send"

        data = {"personalizations": [{
                    "to": [{"email": recipient_email}],
                    "subject": subject
                }],

                "from": {"email": sender_email},

                "content": [{
                    "type": "text/plain",
                    "value": message
                }]
        }

        headers = {
            'authorization': "Bearer {0}".format(api_key),
            'content-type': "application/json"
        }

        response = requests.request("POST", url=url, data=json.dumps(data), headers=headers)

        print("Sent to SendGrid")
        print(response.text)
    elif not sender_email:
        print("No config var for sender email. Add MY_SENDER_EMAIL config var to Heroku!")
    elif not api_key:
        print("No config var for sendgrid api key. Add SENDGRID_API_KEY config var to Heroku!")
    elif not recipient_email:
        print("No recipient email address")
    else:
        print("Unknown error. Aliens.")
