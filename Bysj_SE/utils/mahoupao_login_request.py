import requests
from scrapy.selector import Selector

from Bysj_SE.utils import common_params

session = requests.Session()

def get_formhash():
    st_url = "https://bbs.mahoupao.com/member.php?mod=logging&action=login"
    res = session.get(st_url, headers=common_params.common_headers)
    return Selector(response=res).xpath('//*[@id="layer_reg"]/input[2]/@value').extract_first()

def mahoupao_login(tel, password):
    login_url = "https://bbs.mahoupao.com/plugin.php?id=tshuz_smslogin&mod=login"

    cookie = requests.utils.dict_from_cookiejar(session.cookies)

    formdata = {
        "regsubmit": "yes",
        "formhash" : get_formhash(),
        "referer": "" ,
        "tel" : tel,
        "password" : password,
        "regsubmit" : "true"
    }

    print(formdata["formhash"])
    response = session.post(url=login_url, headers= common_params.common_headers, data= formdata)
    print("登录结果：",response.text)
    return requests.utils.dict_from_cookiejar(session.cookies)

mahoupao_login("15330339432", "wsh2766659938")
