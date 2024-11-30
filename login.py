from datetime import datetime
import requests
from utils import get_login_data

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
session = requests.Session()
session.headers.update({
    "User-Agent": USER_AGENT
})

def issue_to_login_url():
    issue_url = "https://seat-lx.ucass.edu.cn/ic-web/auth/address?finalAddress=https://seat-lx.ucass.edu.cn&errPageUrl=https://seat-lx.ucass.edu.cn/#/error&manager=false&consoleType=16"

    resp = session.get(issue_url, allow_redirects=False)
    json = resp.json()
    
    return json["data"]
    
def issue_form_login_url(to_login):
    resp = session.get(to_login, allow_redirects=False)
    redir = resp.headers["Location"]
    return redir

def login_form(form_url: str, username: str, password: str):
    #to get cookie
    login_resp = session.get(form_url, allow_redirects=False)
    
    login_resp = session.get(form_url, allow_redirects=False)
    # start login
    login_data = get_login_data(session, form_url, username, password)
    
    login_resp = session.post(form_url, data=login_data, allow_redirects=False)
    
    return login_resp

def get_ic_cookie(login_resp: requests.Response):

    url = session.get_redirect_target(login_resp)
    ic_resp = session.get(url, allow_redirects=False)

    url = session.get_redirect_target(ic_resp)
    ic_resp = session.get(url, allow_redirects=False)
    
    return ic_resp.cookies.get_dict()

def login(username, password) -> str | None:
    try:
        to_login_url = issue_to_login_url()
        form_url = issue_form_login_url(to_login_url)
        login_resp = login_form(form_url, username, password)

        ic = get_ic_cookie(login_resp)

        return ic["ic-cookie"]
    except Exception as e:
        print(e)
        return None