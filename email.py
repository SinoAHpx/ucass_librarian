import yagmail

from config import read_config

def send_email(sender, password, recipient, content: str):
    yag = yagmail.SMTP(user=sender, password=password)
    yag.send(recipient, subject="UCASS librarian report", contents=content)