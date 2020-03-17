from util.encode import encode
from util.list_to_json import list_to_json
import requests
import re
import json
from bs4 import BeautifulSoup as bs
import mysql.connector

class School:
    """访问教务系统, 并爬取信息"""

    def __init__(self, id, psw):
        """
        初始化登录
        :param id: 账号
        :param psw: 密码
        """
        self.ses = requests.Session()
        self.id = id
        self.psw = psw
        header = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/76.0.3809.132 Mobile Safari/537.36'
        }
        data = {
            'encoded': self.__encode_data()  # 账号密码加密后的东西
        }
        login_url = 'http://csujwc.its.csu.edu.cn/jsxsd/xk/LoginToXk'
        msg = self.ses.post(login_url, headers=header, data=data, timeout=1000).text  # 这个跳转
        # print(msg)

    def __encode_data(self):
        """
        私有方法加密密码
        :return: 密码密文
        """
        return encode(self.id) + '%%%' + encode(self.psw)

    def get_score(self):
        """
        获取所有分数
        :return: 分数list
        """
        response = self.ses.get('http://csujwc.its.csu.edu.cn/jsxsd/kscj/cjcx_list')
        save = response.content.decode('UTF-8')
        f = open('score.html', 'w+', encoding='UTF-8')
        f.write(save)
        print('下载完成')
        f.close()

    def get_kb(self):
        """
        获取所有课表
        :return: 课表list
        """
        response = self.ses.get('http://csujwc.its.csu.edu.cn/jsxsd/xskb/xskb_list.do')
        save = response.content.decode('UTF-8')
        f = open('kb.html', 'w+', encoding='utf-8')
        f.write(save)
        print('下载完成')
        f.close()

    def get_all_kb(self):
        """
        获取所有的课表
        :return:
        """
        # 校区id
        xqid = ['校本部', '南校区', '铁道校区','湘雅新校区','湘雅老校区','湘雅医院','湘雅二医院','湘雅三医院','新校区']

        # 建筑物id
        for xq in range(len(xqid)):
            response = self.ses.get('http://csujwc.its.csu.edu.cn/kkglAction.do?method=queryjxl&xqid=' + str(xq + 1))
            jzwid = response.text.replace('jzwid', '\'jzwid\'').replace('jzwmc', '\'jzwmc\'')
            jzwid = json.loads(json.dumps(eval(jzwid)))
            # print(jzwid)
            for jzw in jzwid:
                response = self.ses.get('http://csujwc.its.csu.edu.cn/kkglAction.do?method=queryjs&xnxq01id=2019-2020-2&xqid=' + str(xq + 1) + '&jzwid=' + jzw['jzwid'])
                classroom = response.text.split('qz--')[0].replace('jsid', '\'jsid\'').replace('jsmc', '\'jsmc\'')
                # 如果eval(""), 报错
                if classroom != "":
                    classroom = json.loads(json.dumps(eval(classroom)))
                    # print(classroom)

                    for js in classroom:
                        response = self.ses.get('http://csujwc.its.csu.edu.cn/jiaowu/pkgl/llsykb/llsykb_kb.jsp?type=jx0601&isview=1&zc=&xnxq01id=2019-2020-2'
                            + '&xqid=' + str(xq + 1)
                            + '&jzwid=' + jzw['jzwid']
                            + '&classroomID=' + js['jsmc']
                            + '&jx0601id=' + js['jsid'])
                        # print(response.text)
                        soup = bs(response.text)
                        soup.select('#kbtable td ')
                        print(soup.text)
                        break

                # else:
                    # print("该教学楼没有教室可用")

    def post_data(self):
        header = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/76.0.3809.132 Mobile Safari/537.36'
        }
        data = {
            'type': 'jx0601',
            'isview': '1',
            'zc': '',
            'xnxq01id': '2019-2020-2',
            'xqid': '9',
            'jzwid': '901',
            'classroomID': 'A座223',
            'jx0601id': '9010223',
            'jx0601mc': '',
            'sfFD': '1'
        }

        kb_url = 'http://csujwc.its.csu.edu.cn/jiaowu/pkgl/llsykb/llsykb_kb.jsp'
        response = self.ses.post(kb_url, headers=header, data=data)
        # print(response.text)
        html = bs(response.text, 'html.parser')
        table = html.select_one('#kbtable')
        table = bs(str(table), 'html.parser')

        # 获取每个格子中的课表数据
        for index, tr in enumerate(table.find_all('tr')):
            if index != 0:
                tds = tr.find_all('td')
                for i, td in enumerate(tds):
                    print(index, i, td.get_text().strip())

        # 写入到数据库中, 要保证数据库便于查找


if __name__ == '__main__':
    s = School('0902170515', '431124200010313873')
    s.post_data()
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='password',
        database='classroom'
    )
    print(conn.database)

