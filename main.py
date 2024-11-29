import json
from pathlib import Path
from bs4 import BeautifulSoup
import requests

from utils import get_encrypted_pwd, get_login_data, get_random_uuid


USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
GENERAL_HEADERS = {
    'User-Agent': USER_AGENT,
}

def get_cookies(session: requests.Session) -> bool:
    path = Path("cookies.json")
    if path.exists():
        cookies_text = path.read_text()
        cookies_dict = json.loads(cookies_text)
        
        session.cookies.update(cookies_dict)
        
        return True
    else:
        return False

def login(username, password):
    session = requests.Session()
    if not get_cookies(session):
        login_url = "https://authserver.ucass.edu.cn/authserver/login"
        login_data = get_login_data(session, login_url, username, password)

        # cookie should have JESSIONID, springframework
        # expect: 302, cookies
        login_resp = session.post(login_url, data=login_data, allow_redirects=False)
        
        login_do_url = session.get_redirect_target(login_resp)
        login_do_resp = session.get(login_do_url, allow_redirects=False)
        
        index_url = session.get_redirect_target(login_do_resp)
        index_resp = session.get(index_url, allow_redirects=False)
        
        login_api_url = session.get_redirect_target(index_resp)
        login_api_resp = session.get(login_api_url, allow_redirects=False)
        
        ticket_url = session.get_redirect_target(login_api_resp)
        ticket_resp = session.get(ticket_url, allow_redirects=False)
        
        login_center_url = session.get_redirect_target(ticket_resp)
        session.get(login_center_url, allow_redirects=False)
        
        with open('cookies.json', 'w') as f:
            json.dump(session.cookies.get_dict(), f, indent=4)
    
    # index_url = session.get_redirect_target(login_center_resp)
    # index_resp = session.get(index_url, allow_redirects=False)
    
    userConf = session.get('https://authserver.ucass.edu.cn/personalInfo/common/getUserConf')
    userConf_json = userConf.json()
    
    print(f'Welcome {userConf_json["datas"]["cn"][0]}')
    
    return session


def seats_login(login_session: requests.Session):
    seat_session = requests.session()
    
    issue_to_login = 'https://seat-lx.ucass.edu.cn/ic-web/auth/address?finalAddress=https:%2F%2Fseat-lx.ucass.edu.cn&errPageUrl=https:%2F%2Fseat-lx.ucass.edu.cn%2F%23%2Ferror&manager=false&consoleType=16'
    
    issue_to_login_resp = seat_session.get(issue_to_login, allow_redirects=False)
    
    to_login_url = issue_to_login_resp.json()["data"]
    
    to_login_resp = login_session.get(to_login_url, allow_redirects=False)
    
    auth_url = login_session.get_redirect_target(to_login_resp)
    auth_resp = login_session.get(auth_url, allow_redirects=False)

    ticket_url = seat_session.get_redirect_target(auth_resp)
    ticket_resp = seat_session.get(ticket_url, allow_redirects=False)
    
    uni_url = seat_session.get_redirect_target(ticket_resp)
    uni_resp = seat_session.get(uni_url, allow_redirects=True)
    
    secure_ticket_url = ticket_url.replace("http:", "https:")
    secure_ticket_resp = seat_session.get(secure_ticket_url, allow_redirects=True)
    
    
    print(f'Unitoken status code: {uni_resp.status_code}')

    secure_ticket_resp = seat_session.get(secure_ticket_url)
    
    
    return secure_ticket_resp

login_session = login('20241141128', 'frNwzTNNeGnAkkq6ADpAqv*ZGvPHYU')

seats_resp = login_session.get('https://seat-lx.ucass.edu.cn/#/ic/home', allow_redirects=False)

seats_resp = seats_login(login_session)

print(seats_resp.cookies.get_dict())