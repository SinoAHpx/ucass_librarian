import json
from bs4 import BeautifulSoup
import execjs
import requests
import uuid

from rich.console import Console

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
GENERAL_HEADERS = {
    'User-Agent': USER_AGENT,
}

# some global vars
console = Console()
session = requests.Session()


def get_encrypted_pwd(orignal, salt):
    with open('encrypt.js', 'r') as file:
        js_code = file.read()
        
    ctx = execjs.compile(js_code)
    
    result = ctx.call('encryptPassword', orignal, salt)
    
    return result

def get_random_uuid():
    return str(uuid.uuid4()).replace('-', '')

def login(username, password):
    console.print('[bold red]Start login![/bold red]')
    
    uuid = get_random_uuid()
    redirected_response = session.get(f"https://seat-lx.ucass.edu.cn/authcenter/toLoginPage?redirectUrl=https://seat-lx.ucass.edu.cn/ic-web//auth/token?uuid={uuid}&extInfo=", headers=GENERAL_HEADERS, allow_redirects=False)
    
    login_url = redirected_response.headers["Location"]

    console.print(f'User login url: {login_url}')
    
    response = session.get(login_url, allow_redirects=False)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    salt_element = soup.find(id='pwdEncryptSalt')
    execution_element = soup.find(id='execution')
    
    salt = salt_element['value'] if salt_element else ""
    execution = execution_element['value'] if execution_element else ""
    encrypted_password = get_encrypted_pwd(password, salt)

    # 4. Prepare login data
    login_data = {
        "username": username,
        "password": encrypted_password,
        "captcha": "",  # If needed
        "_eventId": "submit",
        "lt": "",
        "pwdEncryptSalt": salt,
        "cllt": "userNameLogin",
        "dllt": "generalLogin",
        "execution": execution,
    }
    
    console.print(f'Login with data [red]{login_data}[/red]')
    
    console.print(f'Login cookie: [red]{session.cookies}[/red]')

    response = session.post(login_url, data=login_data, allow_redirects=False)
    
    console.print(f'Login response headers: [red]{response.headers}[/red]')
    
    ticket_url = response.headers["Location"]
    print(f'ticket url: {ticket_url}')
    
    ticket_response = session.get(ticket_url, allow_redirects=False)
    unitoken_url = ticket_response.headers["Location"]
    print(f'unitoken url: {unitoken_url}')

    unitoken_response = session.get(unitoken_url, allow_redirects=False)
    console.print(f'unitoken code: [green]{unitoken_response.status_code}[/green]')
    
    secure_tiket_url = ticket_url.replace("http:", "https:")
    secure_tiket_response = session.get(secure_tiket_url, allow_redirects=False)
    
    print(secure_tiket_response)
    
    return response

def ticket_auth(url: str, use_https: bool = False) -> requests.Response:
    if use_https:
        url = url.replace("http://", "https://")
    
    response = session.get(url, allow_redirects=False)
    
    return response

def get_ic_cookies():
    console.print(f'[red]Start get ic cookies![/red]')

    uuid = get_random_uuid()
    alreay_login_response = session.get(f"https://seat-lx.ucass.edu.cn/authcenter/toLoginPage?redirectUrl=https://seat-lx.ucass.edu.cn/ic-web//auth/token?uuid={uuid}&extInfo=", allow_redirects=False)
    console.print(f'alreay login status code: [yellow]{alreay_login_response.status_code}[/yellow]')
    
    login_url = alreay_login_response.headers["Location"]
    
    # yes again
    console.print(f'Cookie request login url: [red]{login_url}[/red]')
    
    # this session cookie should be saved
    response = session.get(login_url, allow_redirects=False)
    console.print(f'GET login status code: [yellow]{response.status_code}[/yellow]')
    
    ticket_url = response.headers["Location"]
    ticket_response = ticket_auth(ticket_url)
    
    unitoken_url = ticket_response.headers["Location"]
    console.print(f'ticket unitoken url: [red]{unitoken_url}[/red]')
    console.print(f'ticket auth status: [yellow]{ticket_response.status_code}[/yellow]')
    uni_response = session.get(unitoken_url)
    
    console.print(f'unitoken get: [green]{uni_response.status_code}[/green]')
    
    console.print('[red]Starting final hit[/red]')
    ticket_response = ticket_auth(ticket_url, True)
    console.print(f'ticket auth status: [yellow]{ticket_response.status_code}[/yellow]')
    console.print(f'ticket headers: {ticket_response.headers}')
    
    return ticket_response

login_response = login('20241141128', 'frNwzTNNeGnAkkq6ADpAqv*ZGvPHYU')
login_cookies = login_response.cookies

# login_cookies = {
#     "happyVoyage": "Pqh6Qyak3s4YrkG0DTLC//GJxJaPhOQsLsU7MoZjA6aui0Qw7/6IgweEucvo+TAOp5BSKNV9ybhz8pYYSpCs1gma/eD+oP679oQhMCNd/cJzjFgkFFmFJyTQtiAJUw3cUwoZoxDeBwND8U2dGMI42QU7IXm88D4ob1ikoPFp81U=",
#     "CASTGC": "TGT-568719-jrs08ja-RMNPaxJm9w5Noxz6JOUnJ6hPnHdDKj8ywLMRi3Xm4IynfwpGS0SCJbcZKqEnull_main",
#     "JSESSIONID": "84AE62F8A8928808ECB4D9A499C50C09",
#     "org.springframework.web.servlet.i18n.CookieLocaleResolver.LOCALE": "en"
# }
cookies = get_ic_cookies()

print(cookies.cookies.get_dict())