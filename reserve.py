from datetime import datetime, timedelta
import requests

session = requests.Session()

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
    
    code = resp["code"]
    if code == 0:
        dev = resp["data"]["resvDevInfoList"][0]["devName"]
        print(f'{dev} has been successfully reserved.')
        return True
    else:
        print('login was expired, please another login.')
        return False

def get_seats_info(ic: str, room_id: int, date: datetime):
    session.cookies.update({"ic-cookie": ic})
    date = date.strftime("%Y%m%d")
    url = f"https://seat-lx.ucass.edu.cn/ic-web/reserve?roomIds={room_id}&resvDates={date}&sysKind=8"
    
    resp = session.get(url)
    json = resp.json()
    
    if json["code"] != 0:
        print('Some error, maybe you are not login')
        return
    
    return json

def get_available_seats(json):
    # session.cookies.update({"ic-cookie": ic})
    
    data = json["data"]
    
    for seat in data:
        if len(seat["resvInfo"]) == 0:
            continue
        info = seat["resvInfo"][0]
        start = datetime.fromtimestamp(info["startTime"] / 1000)
        initial = start.replace(hour=8, minute=0, second=0)
        print(f'Seat: {seat["devName"]} / {start}')
        continue
        if start - initial > timedelta(hours=4):
            print(f'Seat: {seat["devName"]} / {start}')
        
# json = get_seats_info("83f1257b-47fd-4d8a-9bb3-ffc8f4e29d65", 100236920, datetime.now() + timedelta(days=1))
# get_available_seats(json)