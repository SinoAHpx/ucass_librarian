# Login

*GET* https://seat-lx.ucass.edu.cn/authcenter/toLoginPage?redirectUrl=https%3A%2F%2Fseat-lx.ucass.edu.cn%2Fic-web%2F%2Fauth%2Ftoken%3Fuuid%3D300259b94017464e9392c2a5ffa3ce2c&extInfo=
with an random uuid as query parameter
- form login url

after form login *POST*:
- cookies:
    - happyVoyage
    - CASTGC
- headers:
    - Location sample: http://seat-lx.ucass.edu.cn/authcenter/doAuth/aeeb72b40d3848fda8493b70aea57588?ticket= **ST-2065755-V9-W1Z3WY40P-3O65Ls6cDZwdlAciapserver1**

send *GET* to login *Location* header url:
- get another *Location* url
    - uuid: d628443c07d434b9e07fd39f6ef545a
    - unitoken: eyJhbGciOiJIUzUxMiIsImNhbGciOiJHWklQIn0.H4sIAAAAAAAAAGVQu47CMBD8F9cpkhwSHC1paGhChyhW3j3OJz8iey0FIf4dny6xjU5yMzua8cw8hHY3ZU9gSOxF3_abrkuv34lGsI_0R9iodSMkeDy5FSk8JLwikNJFy4Uky4OSB4dFriGE2g9p4hob-HG-PgSa3wzznYFjWBEZUDrnQPQUMjd9O1sCxMDODMCQpZbJn-9TiUAmF5TzmP4p6rkus_QdlySXazKbJ-UJh0oTUhTl7DHPpH6jiWjVV1Jj2hgi_ts9GYl9t_3od2372bXPFyvu8WSkAQAA.IhW9uFR4T9ASFVmnTiMYg2HOG5n1D2n4sZqGEJ8Ss8oC7smg4asETlsqBznXRFNfvK2u4mHA45oj6v0NVR3q4A


*GET Location with uuid and unitoken*:
- Stautus code: 200

# Get cookie

*GET* https://seat-lx.ucass.edu.cn/authcenter/toLoginPage 
> with antoher random uuid

*GET* https://authserver.ucass.edu.cn/authserver/login?service=http%3A%2F%2Fseat-lx.ucass.edu.cn%2Fauthcenter%2FdoAuth%2Fe2c1749a8f5a461b82b256601d8dec80
> with previous uuid
> with cookie from Login section
    - JSESSIONID
    - CASTGC
    - springframework
    - happyVoyage

retrieve: 
- Cookies
    - another happyVoyage
    - Path
    - HttpOnly
- Headers:
    - Location: lx.ucass.edu.cn/authcenter/doAuth/e2c1749a8f5a461b82b256601d8dec80?ticket=
    *ST-2065770-oSzloANGynEr1tC9mY4P21-nDdwciapserver1*

*GET* Location with ticket
- Headers
    - Location: *uuid* and *unitoken*

*GET* Location with ticket, https ver
- Cookies:
    - **ic_cookie**




<RequestsCookieJar[Cookie(version=0, name='happyVoyage', value='8RxWc/YhdPecWL5o9Sne61lCMIdWQEc5RcAp5fINLYay28kenkN0++gI86ZZwr4FN70+2Y1cGfmoC47OeQsmWpi47umPpMV4Y3duZ1CSK/DRmW/oOofds2BAXjuUledp44lmTbcHhbCSdVtNSq3ohCVmJ8lynZN8uqbBDsGX4Jw=', port=None, port_specified=False, domain='authserver.ucass.edu.cn', domain_specified=False, domain_initial_dot=False, path='/', path_specified=True, secure=False, expires=None, discard=True, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False), Cookie(version=0, name='platformMultilingual', value='en', port=None, port_specified=False, domain='.edu.cn', domain_specified=True, domain_initial_dot=False, path='/', path_specified=True, secure=False, expires=None, discard=True, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False)]>

<RequestsCookieJar[Cookie(version=0, name='JSESSIONID', value='58280A135B8F7EE08D2B367B4E3F242C', port=None, port_specified=False, domain='authserver.ucass.edu.cn', domain_specified=False, domain_initial_dot=False, path='/authserver', path_specified=True, secure=True, expires=None, discard=True, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False), Cookie(version=0, name='CASTGC', value='TGT-568739-g6HChjGWoOdNMAm8Q0HrnI5dr2pnCFKbp1-0K5DweogtEWKRNd90m6Grl3WweF88hc8null_main', port=None, port_specified=False, domain='authserver.ucass.edu.cn', domain_specified=False, domain_initial_dot=False, path='/authserver', path_specified=True, secure=False, expires=None, discard=True, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False), Cookie(version=0, name='happyVoyage', value='AT9CboVhRRgAYHM9CUpCHPqmO5QnCtjotG6XAOl14hNPcDfSwl+yNv0YWXA9PauOrygDrmZus6HOGzAKsVG5RImGbFgFaThGR7m2BYGEbBdHZjtrTA5tqRGwrjq32iFJjT2Ec7nDYOmj+YB4tsbJ6yhKODiUsB8d8yufWgMEVTk=', port=None, port_specified=False, domain='authserver.ucass.edu.cn', domain_specified=False, domain_initial_dot=False, path='/', path_specified=True, secure=False, expires=None, discard=True, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False), Cookie(version=0, name='platformMultilingual', value='zh_CN', port=None, port_specified=False, domain='.edu.cn', domain_specified=True, domain_initial_dot=False, path='/', path_specified=True, secure=False, expires=None, discard=True, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False)]>