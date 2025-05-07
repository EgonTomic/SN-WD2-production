import json
import os
import requests

def send_email(receiver_email, subject, text):
    sender_mail = os.getenv("MY_SENDER_EMAIL", "egontomic75@gmail.com")
    api_key = os.getenv("API_KEY", "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")

    if sender_mail and api_key:
        url = "https://api.sendgrid.com/v3/mail/send"
        
        data = {"personalizations": [{
                "to": [{"email": receiver_email}],
                "subject": subject
            }],
            "from": {"email": sender_mail},
            "content": [{"type": "text/plain",
                         "value": text}]
        }

        headers = { "authorization": "Bearer {0}".format(api_key),
                   "content-type": "application/json"}
        
        response = requests.request("POST", url=url, data=json.dumps(data), headers=headers)
        print("Email sent to sendgrid")
        print(response.text)
    else:
        print("No env vars or no email address")