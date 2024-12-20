from bs4 import BeautifulSoup
import requests
import uuid

from encrypt import encrypt_password

def get_encrypted_pwd(password, salt):
    result = encrypt_password(password, salt)
    
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