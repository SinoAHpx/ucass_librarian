import json
from bs4 import BeautifulSoup
import execjs
import requests
import uuid

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
GENERAL_HEADERS = {
    'User-Agent': USER_AGENT,
}

session = requests.Session()


def get_encrypted_pwd(password, salt):
    with open('encrypt.js', 'r') as file:
        js_code = file.read()
        
    ctx = execjs.compile(js_code)
    
    result = ctx.call('encryptPassword', password, salt)
    
    return result

def get_random_uuid():
    return str(uuid.uuid4()).replace('-', '')

def login(username, password):
    request_uuid = get_random_uuid()
    redirect_resp = session.get(f"https://seat-lx.ucass.edu.cn/authcenter/toLoginPage?redirectUrl=https://seat-lx.ucass.edu.cn/ic-web//auth/token?uuid={request_uuid}&extInfo=", headers=GENERAL_HEADERS, allow_redirects=False)
    
    login_url = "https://authserver.ucass.edu.cn/authserver/login?service=http%3A%2F%2Fseat-lx.ucass.edu.cn%2Fauthcenter%2FdoAuth%2F6113ee0c8b244a1792bad68392a1672c"
    
    login_resp = session.get(login_url, allow_redirects=False)
    
    soup = BeautifulSoup(login_resp.text, 'html.parser')
    
    salt_element = soup.find(id='pwdEncryptSalt')
    execution_element = soup.find(id='execution')
    
    salt = salt_element['value'] if salt_element else ""
    execution = execution_element['value'] if execution_element else ""
    encrypted_password = get_encrypted_pwd(password, salt)

    login_data = {
        "username": username,
        "password": encrypted_password,
        "captcha": "",
        "_eventId": "submit",
        "lt": "",
        "pwdEncryptSalt": salt,
        "cllt": "userNameLogin",
        "dllt": "generalLogin",
        "execution": execution,
    }

    auth_resp = session.post(login_url, data=login_data, allow_redirects=False)
    
    ticket_url = auth_resp.headers["Location"]
    ticket_resp = session.get(ticket_url, allow_redirects=False)
    unitoken_url = ticket_resp.headers["Location"]

    unitoken_resp = session.get(unitoken_url, allow_redirects=False)
    
    secure_ticket_url = ticket_url.replace("http:", "https:")
    secure_ticket_resp = session.get(secure_ticket_url, allow_redirects=False)
    
    return auth_resp

def ticket_auth(url: str, use_https: bool = False) -> requests.Response:
    if use_https:
        url = url.replace("http://", "https://")
    
    auth_resp = session.get(url, allow_redirects=False)
    
    return auth_resp

def get_ic_cookies():
    request_uuid = get_random_uuid()
    login_redirect_resp = session.get(f"https://seat-lx.ucass.edu.cn/authcenter/toLoginPage?redirectUrl=https://seat-lx.ucass.edu.cn/ic-web//auth/token?uuid={request_uuid}&extInfo=", allow_redirects=False)
    
    login_url = login_redirect_resp.headers["Location"]
    
    login_resp = session.get(login_url, allow_redirects=False)
    
    ticket_url = login_resp.headers["Location"]
    ticket_resp = ticket_auth(ticket_url)
    
    unitoken_url = ticket_resp.headers["Location"]
    
    unitoken_resp = session.get(unitoken_url)
    
    final_ticket_resp = ticket_auth(ticket_url, True)
    
    return final_ticket_resp

login_response = login('20241141128', 'frNwzTNNeGnAkkq6ADpAqv*ZGvPHYU')
login_cookies = login_response.cookies

cookies = get_ic_cookies()