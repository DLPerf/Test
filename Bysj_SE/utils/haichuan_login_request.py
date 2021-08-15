import requests
from scrapy.selector import Selector

from Bysj_SE.utils import common_params

session = requests.Session()
def get_formhash():
    st_url = "https://bbs.hcbbs.com/plugin.php?id=it618_members:login"
    res = session.get(st_url, headers=common_params.common_headers)
    return Selector(response=res).xpath('//input[@name="formhash"]/@value').extract_first()

def haichuan_login(username, password):
    login_url = "https://bbs.hcbbs.com/plugin.php?id=it618_members:ajax&ac=login&formhash=" + get_formhash()
    cookie = requests.utils.dict_from_cookiejar(session.cookies)
    formdata = {
        "version": "v7.5.3",
        "logintype": "1",
        "username": username,
        "password": password,
        "validatecode": '',
        "usertelcode": '',
        "userquestionid": "0",
        "useranswer": ''
    }
    response = session.post(url=login_url, headers= common_params.common_headers, data= formdata)
    print("登录结果：",response.text)
    return requests.utils.dict_from_cookiejar(session.cookies)

# haichuan_login("Crown-w", "wsh2766659938")