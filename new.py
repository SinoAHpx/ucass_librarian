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

def login(username, password):
    to_login_url = issue_to_login_url()
    form_url = issue_form_login_url(to_login_url)
    login_resp = login_form(form_url, username, password)

    ic = get_ic_cookie(login_resp)

    return ic["ic-cookie"]

def get_lib_user_info(ic: str):
    url = "https://seat-lx.ucass.edu.cn/ic-web/auth/userInfo"

    session.cookies.update({"ic-cookie": ic})

    resp = session.get(url)
    json = resp.json()

    return json

# result is to indicate whether a re-login is needed
def reserve(ic: str, seat: int, start_time: datetime, end_time: datetime) -> bool:
    if start_time < datetime.now() or end_time < datetime.now():
        print('start time or end time should not be ealier than current time. ')
        return True
    
    url = "https://seat-lx.ucass.edu.cn/ic-web/reserve"

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
    

# reserve_params = {
#     'ic': "84d6850c-7079-4d94-8f3f-c1b826a95dad",
#     'seat': 100237659,
#     'start_time': datetime(2024,11,29,20,00,00),
#     'end_time': datetime(2024,11,29,22,00,00)
# }
# if not reserve(**reserve_params):
#     ic = login("20241141128", "frNwzTNNeGnAkkq6ADpAqv*ZGvPHYU")
#     print(ic)
#     reserve_params["ic"] = ic
#     reserve(**reserve_params)


ic = login("20241141128", "frNwzTNNeGnAkkq6ADpAqv*ZGvPHYU")
print(ic)

# j = get_lib_user_info("68435aaf-32bd-4549-be70-85e80c005a9c")
# print(j)