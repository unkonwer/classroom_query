from encode_util.encode import encode
import requests
import re


class School:
    """访问教务系统, 并爬取信息"""

    def __init__(self, id, psw):
        self.ses = requests.session()
        self.id = id
        self.psw = psw

    def encode_data(self):
        return encode(self.id) + '%%%' + encode(self.psw)

    def login(self):
        header = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/76.0.3809.132 Mobile Safari/537.36'
        }
        data = {
            'encoded': self.encode_data()  # 账号密码加密后的东西
        }
        url = 'http://csujwc.its.csu.edu.cn/jsxsd/xk/LoginToXk'
        msg = self.ses.post(url, headers=header, data=data, timeout=1000).text  # 这个跳转
        return self.ses.cookies

    def get_classroom(self):
        header = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/76.0.3809.132 Mobile Safari/537.36',
            'cookies': self.login()
        }
        data = {
            'type': 'jx0601',
            'isview': '1',
            'zc': '',
            'xnxq01id': '2019-2020-1',
            'xqid': '',
            'jzwid': '',
            'classroomID': 'B座101',
            'jx0601id': '9020101',
            'jx0601mc': '',
            'sfFD': '1'
        }
        url = 'http://csujwc.its.csu.edu.cn/jiaowu/pkgl/llsykb/llsykb_kb.jsp'
        msg = self.ses.post(url, headers=header, data=data, timeout=1000).text
        return msg


if __name__ == '__main__':
    s = School('0902170515', '431124200010313873')
    print(s.encode_data())
    print(s.get_classroom())
