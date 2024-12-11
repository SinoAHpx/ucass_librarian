import yagmail

from config import read_config

def send_email(content: str):
    conf = read_config()
    if conf == None:
        return
    
    yag = yagmail.SMTP(user=conf.notifier.gmail, password=conf.notifier.password)
    yag.send(conf.notifier.recipient, subject="UCASS librarian report", contents=content)