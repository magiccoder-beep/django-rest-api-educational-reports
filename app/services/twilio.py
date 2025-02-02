from twilio.rest import Client
import os

class TwilioService:
    def __init__(self):
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.client = Client(self.account_sid, self.auth_token)

    def send_sms(self, to, from_, body):
        message = self.client.messages.create(
            body=body,
            from_=from_,
            to=to
        )
        return message.sid

    def make_call(self, to, from_, url):
        call = self.client.calls.create(
            url=url,
            to=to,
            from_=from_
        )
        return call.sid

# Example usage:
# twilio_service = TwilioService()
# sms_sid = twilio_service.send_sms('+1234567890', '+0987654321', 'Hello from Twilio!')
# call_sid = twilio_service.make_call('+1234567890', '+0987654321', 'http://demo.twilio.com/docs/voice.xml')