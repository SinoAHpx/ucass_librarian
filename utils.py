from bs4 import BeautifulSoup
import requests
import uuid
import execjs


def get_encrypted_pwd(password, salt):
    with open('encrypt.js', 'r') as file:
        js_code = file.read()
        
    ctx = execjs.compile(js_code)
    
    result = ctx.call('encryptPassword', password, salt)
    
    return result

def get_random_uuid():
    return str(uuid.uuid4()).replace('-', '')

def get_login_data(session: requests.Session, login_url, username, password):
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
    
    return login_data