from datetime import datetime
import requests
from utils import get_login_data

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

def issue_to_login_url():
    issue_url = "https://seat-lx.ucass.edu.cn/ic-web/auth/address?finalAddress=https://seat-lx.ucass.edu.cn&errPageUrl=https://seat-lx.ucass.edu.cn/#/error&manager=false&consoleType=16"
    headers = {
        "sec-ch-ua-platform": "\"macOS\"",
        "user-agent": USER_AGENT,
        "accept": "application/json, text/plain, */*",
        "sec-ch-ua": "\"Not_A_Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"",
        "sec-ch-ua-mobile": "?0",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "priority": "u=1"
    }
    
    resp = requests.get(issue_url, headers=headers, allow_redirects=False)
    json = resp.json()
    
    return json["data"]
    
def issue_form_login_url(to_login):
    headers = {
        "sec-ch-ua-platform": "\"macOS\"",
        "user-agent": USER_AGENT,
        "accept": "application/json, text/plain, */*", 
        "sec-ch-ua": "\"Not_A_Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"",
        "sec-ch-ua-mobile": "?0",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "priority": "u=1"
    }
    
    resp = requests.get(to_login, headers=headers, allow_redirects=False)
    redir = resp.headers["Location"]
    return redir

def login_form(form_url: str, username: str, password: str):
    login_session = requests.Session()
    headers = {
        "sec-ch-ua-platform": "\"macOS\"",
        "user-agent": USER_AGENT,
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "sec-ch-ua": "\"Not_A_Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"", 
        "sec-ch-ua-mobile": "?0",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "navigate",
        "sec-fetch-dest": "document",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "priority": "u=0, i"
    }
    
    #to get cookie
    login_resp = login_session.get(form_url, headers=headers, allow_redirects=False)
    
    headers = {
        **headers,
        # "cookie": login_session.cookies.get_dict()["JSESSIONID"],
        "referer": form_url
    }
    
    login_resp = login_session.get(form_url, headers=headers, allow_redirects=False)
    # start login
    login_data = get_login_data(login_session, form_url, username, password)
    
    login_resp = login_session.post(form_url, data=login_data, allow_redirects=False)
    
    return login_session, login_resp

def get_ic_cookie(login_resp: requests.Response):
    ic_session = requests.Session()
    headers = {
        "sec-ch-ua-platform": "\"macOS\"",
        "user-agent": USER_AGENT,
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "sec-ch-ua": "\"Not_A_Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"",
        "sec-ch-ua-mobile": "?0",
        "sec-fetch-site": "same-origin", 
        "sec-fetch-mode": "navigate",
        "sec-fetch-dest": "document",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "priority": "u=0, i"
    }
    
    url = ic_session.get_redirect_target(login_resp)
    ic_resp = ic_session.get(url, headers=headers, allow_redirects=False)
    print(url)
    
    url = ic_session.get_redirect_target(ic_resp)
    ic_resp = ic_session.get(url, headers=headers, allow_redirects=False)
    print(url)
    
    return ic_resp.cookies.get_dict()

def login(username, password):
    to_login_url = issue_to_login_url()
    form_url = issue_form_login_url(to_login_url)
    _, login_resp = login_form(form_url, username, password)

    ic = get_ic_cookie(login_resp)

    return ic["ic-cookie"]

def get_lib_user_info(ic: str):
    url = "https://seat-lx.ucass.edu.cn/ic-web/auth/userInfo"
    session = requests.Session()

    session.cookies.update({"ic-cookie": ic})

    resp = session.get(url)
    json = resp.json()

    return json


def reserve(ic: str, seat: int, start_time: datetime, end_time: datetime) -> bool:
    url = "https://seat-lx.ucass.edu.cn/ic-web/reserve"
    session = requests.Session()
    
    json = get_lib_user_info(ic)
    if json["code"] != 0:
        print('Login expired')
        return False
    
    json = json["data"]
    
    session.cookies.update({
        "qqmail_alias": f'{json["pid"]}@ucass.edu.cn',
        "perf_dv6Tr4n": "1",
        "ic-cookie": ic
    })
    
    payload = {
        "sysKind": 8,
        "appAccNo": json["accNo"],
        "memberKind": 1,
        "resvMember": [
            json["accNo"]
        ],
        "resvBeginTime": start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "resvEndTime":  end_time.strftime("%Y-%m-%d %H:%M:%S"),
        "resvProperty": 0,
        "resvDev": [
            seat
        ]
    }

    resp = session.post(url, json=payload)
    resp = resp.json()    
    
    if resp["code"] == 0:
        dev = resp["data"]["resvDevInfoList"][0]["devName"]
        print(f'{dev} has been successfully reserved.')
        return True
    else:
        print('login was expired, please another login.')
        return False

def get_seat_menu():
    url = "https://seat-lx.ucass.edu.cn/ic-web/seatMenu"
    

reserve_params = {
    'ic': "986b3fb0-8bf6-49cb-8b75-6f65e8f5b6aa",
    'seat': 100237659,
    'start_time': datetime(2024,11,29,20,00,00),
    'end_time': datetime(2024,11,29,22,00,00)
}
if not reserve(**reserve_params):
    ic = login("20241141128", "frNwzTNNeGnAkkq6ADpAqv*ZGvPHYU")
    reserve_params["ic"] = ic
    reserve(**reserve_params)




# j = get_lib_user_info("68435aaf-32bd-4549-be70-85e80c005a9c")
# print(j)