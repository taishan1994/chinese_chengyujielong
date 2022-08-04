# coding=utf-8
import os
import re
import codecs
import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url1 = "http://chengyu.t086.com/"
base_url2 = "https://chengyu.qianp.com/"
base_url3 = "https://cy.hwxnet.com/"

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}


def get_all_chengyu1():
    p1 = "ABCDEFGHJKLMNOPQRSTWXYZ"
    p2 = 100
    cy_urls = []
    cys = []
    for pp1 in p1:
        for pp2 in range(1, p2):
            url = os.path.join(base_url1, "list/{}_{}.html".format(pp1, pp2))
            print(url)
            data = requests.get(url)
            data.encoding = data.apparent_encoding
            html = data.text
            soup = BeautifulSoup(html, "lxml")
            # 超出了页数范围捕获异常
            try:
                div = soup.find('div', {"class": "listw"})
                ul = div.find("ul")
                lis = ul.find_all("li")
                for li in lis:
                    a = li.find("a")
                    cy_url = a.get("href")
                    cy_urls.append(cy_url)
                    cy = li.text
                    cys.append(cy)
            except Exception as e:
                print(e)
                break
    data = {
        "成语链接": cy_urls,
        "成语": cys,
    }
    data = pd.DataFrame(data)
    data.to_csv("data/cym1.csv")


def get_all_chengyu2():
    p1 = "ABCDEFGHJKLMNOPQRSTWXYZ".lower()
    p2 = 100
    cy_urls = []
    cys = []
    for pp1 in p1:
        for pp2 in range(1, p2):
            url = os.path.join(base_url2, "szm_{}_p{}.html".format(pp1, pp2))
            print(url)
            data = requests.post(url, headers=headers)
            data.encoding = data.apparent_encoding
            html = data.text
            soup = BeautifulSoup(html, "lxml")
            # 超出了页数范围捕获异常
            try:
                ul = soup.find('ul', {"class": "btn w4"})
                lis = ul.find_all("li")
                for li in lis:
                    a = li.find("a")
                    cy_url = a.get("href")
                    cy_urls.append(cy_url)
                    cy = re.search("</span>(.*?)</a>", str(a))
                    cys.append(cy.groups()[0])
            except Exception as e:
                print(e)
                break
    data = {
        "成语链接": cy_urls,
        "成语": cys,
    }
    data = pd.DataFrame(data)
    data.to_csv("data/cym2.csv")


def get_all_chengyu3():
    """
    p1 = ["a", "ba", "ca", "da", "e", "fa", "ga",
          "ha",
          "ji",
          "kai",
          "la",
          "ma",
          "na",
          "o",
          "pa",
          "qi",
          "ran",
          "sa",
          "ta",
          "wa",
          "xi",
          "ya",
          "za"]
    p2 = []
    for pp1 in p1:
        url = os.path.join(base_url3, "pinyin/{}.html".format(pp1))
        data = requests.post(url, headers=headers)
        data.encoding = data.apparent_encoding
        html = data.text
        # 找到所有的的拼音
        soup = BeautifulSoup(html, "lxml")
        a_all = soup.find_all("a", {"class": "pinyin_sub_idx"})
        for a in a_all:
            p2.append(a.text)
    """
    p2 = ['a', 'ai', 'an', 'ang', 'ao', 'ba', 'bai', 'ban', 'bang', 'bao', 'bei', 'ben', 'beng', 'bi', 'bian', 'biao',
          'bie', 'bin', 'bing', 'bo', 'bu', 'ca', 'cai', 'can', 'cang', 'cao', 'ce', 'cen', 'ceng', 'cha', 'chai',
          'chan', 'chang', 'chao', 'che', 'chen', 'cheng', 'chi', 'chong', 'chou', 'chu', 'chuai', 'chuan', 'chuang',
          'chui', 'chun', 'chuo', 'ci', 'cong', 'cu', 'cuan', 'cui', 'cun', 'cuo', 'da', 'dai', 'dan', 'dang', 'dao',
          'de', 'deng', 'di', 'dian', 'diao', 'die', 'ding', 'diu', 'dong', 'dou', 'du', 'duan', 'dui', 'dun', 'duo',
          'e', 'en', 'er', 'fa', 'fan', 'fang', 'fei', 'fen', 'feng', 'fo', 'fou', 'fu', 'ga', 'gai', 'gan', 'gang',
          'gao', 'ge', 'gen', 'geng', 'gong', 'gou', 'gu', 'gua', 'guai', 'guan', 'guang', 'gui', 'gun', 'guo', 'ha',
          'hai', 'han', 'hang', 'hao', 'he', 'hei', 'hen', 'heng', 'hong', 'hou', 'hu', 'hua', 'huai', 'huan', 'huang',
          'hui', 'hun', 'huo', 'ji', 'jia', 'jian', 'jiang', 'jiao', 'jie', 'jin', 'jing', 'jiong', 'jiu', 'ju', 'juan',
          'jue', 'jun', 'kai', 'kan', 'kang', 'kao', 'ke', 'ken', 'keng', 'kong', 'kou', 'ku', 'kua', 'kuai', 'kuan',
          'kuang', 'kui', 'kun', 'kuo', 'la', 'lai', 'lan', 'lang', 'lao', 'le', 'lei', 'leng', 'li', 'lian', 'liang',
          'liao', 'lie', 'lin', 'ling', 'liu', 'long', 'lou', 'lu', 'luan', 'lue', 'lun', 'luo', 'lv', 'lve', 'ma',
          'mai', 'man', 'mang', 'mao', 'mei', 'men', 'meng', 'mi', 'mian', 'miao', 'mie', 'min', 'ming', 'miu', 'mo',
          'mou', 'mu', 'na', 'nai', 'nan', 'nang', 'nao', 'ne', 'nei', 'nen', 'neng', 'ni', 'nian', 'niao', 'nie',
          'ning', 'niu', 'nong', 'nu', 'nuan', 'nuo', 'nv', 'nve', 'o', 'ou', 'pa', 'pai', 'pan', 'pang', 'pao', 'pei',
          'pen', 'peng', 'pi', 'pian', 'piao', 'pie', 'pin', 'ping', 'po', 'pou', 'pu', 'qi', 'qia', 'qian', 'qiang',
          'qiao', 'qie', 'qin', 'qing', 'qiong', 'qiu', 'qu', 'quan', 'que', 'qun', 'ran', 'rang', 'rao', 're', 'ren',
          'reng', 'ri', 'rong', 'rou', 'ru', 'ruan', 'rui', 'run', 'ruo', 'sa', 'sai', 'san', 'sang', 'sao', 'se',
          'sen', 'seng', 'sha', 'shai', 'shan', 'shang', 'shao', 'she', 'shen', 'sheng', 'shi', 'shou', 'shu', 'shua',
          'shuai', 'shuan', 'shuang', 'shui', 'shun', 'shuo', 'si', 'song', 'sou', 'su', 'suan', 'sui', 'sun', 'suo',
          'ta', 'tai', 'tan', 'tang', 'tao', 'te', 'teng', 'ti', 'tian', 'tiao', 'tie', 'ting', 'tong', 'tou', 'tu',
          'tuan', 'tui', 'tun', 'tuo', 'wa', 'wai', 'wan', 'wang', 'wei', 'wen', 'weng', 'wo', 'wu', 'xi', 'xia',
          'xian', 'xiang', 'xiao', 'xie', 'xin', 'xing', 'xiong', 'xiu', 'xu', 'xuan', 'xue', 'xun', 'ya', 'yan',
          'yang', 'yao', 'ye', 'yi', 'yin', 'ying', 'yong', 'you', 'yu', 'yuan', 'yue', 'yun', 'za', 'zai', 'zan',
          'zang', 'zao', 'ze', 'zei', 'zen', 'zeng', 'zha', 'zhai', 'zhan', 'zhang', 'zhao', 'zhe', 'zhen', 'zheng',
          'zhi', 'zhong', 'zhou', 'zhu', 'zhua', 'zhuai', 'zhuan', 'zhuang', 'zhui', 'zhun', 'zhuo', 'zi', 'zong',
          'zou', 'zu', 'zuan', 'zui', 'zun', 'zuo']
    cy_urls = []
    cys = []
    for pp1 in p2:
        url = os.path.join(base_url3, "pinyin/{}.html".format(pp1))
        print(url)
        data = requests.post(url, headers=headers)
        data.encoding = data.apparent_encoding
        html = data.text
        soup = BeautifulSoup(html, "lxml")
        # 超出了页数范围捕获异常
        try:
            ul = soup.find('ul', {"class": "pinyin_ul"})
            lis = ul.find_all("li")
            for li in lis:
                a = li.find("a")
                cy_url = a.get("href")
                cy_urls.append(cy_url)
                cy = a.text
                cys.append(cy)
        except Exception as e:
            print(e)
            break
    data = {
        "成语链接": cy_urls,
        "成语": cys,
    }
    data = pd.DataFrame(data)
    data.to_csv("data/cym3.csv")

def parse_url3_detail():
    data = pd.read_csv("data/cym3.csv", encoding="utf-8")
    cys = []  # 成语
    pys = []  # 拼音
    cyjs = []  # 成语解释
    dgcc = [] # 典故出处
    jyc = [] # 近义词
    fyc = [] # 反义词
    cycd = [] # 常用程度
    gqsc = [] # 感情色彩
    yfyf = [] # 语法用法
    cyjg = [] # 成语结构
    csnd = [] # 产生年代
    ywfy = [] # 英文翻译
    cymm = [] # 成语谜面
    cur = 1
    total = len(data)
    for j,d in enumerate(data.itertuples()):
        print(cur, total)
        cur = cur + 1
        url = d[2]
        cy = d[3]
        url = os.path.join(base_url3, url)
        data = requests.post(url, headers=headers)
        data.encoding = data.apparent_encoding
        html = data.text
        soup = BeautifulSoup(html, "lxml")
        pinyin = soup.find("span", {"class":"pinyin f20"}).text
        pys.append(pinyin)
        div = soup.find("div", {"class":"view_con clearfix"})
        dl = div.find("dl")
        dts = dl.find_all("dt")
        dds = dl.find_all("dd")
        cys.append(cy)
        for dt,dd in zip(dts, dds):
            cate = dt.text.replace('[', '')
            cate = cate.replace(']', '')
            cate = cate.strip()
            content = dd.text
            content = content.strip()
            # print(cate, content)
            if cate == "成语解释":
                cyjs.append(content)
            elif cate == "典故出处":
                dgcc.append(content)
            elif cate == "近义词":
                jyc.append(content)
            elif cate == "反义词":
                fyc.append(content)
            elif cate == "常用程度":
                cycd.append(content)
            elif cate == "感情色彩":
                gqsc.append(content)
            elif cate == "语法用法":
                yfyf.append(content)
            elif cate == "成语结构":
                cyjg.append(content)
            elif cate == "产生年代":
                csnd.append(content)
            elif cate == "英文翻译":
                ywfy.append(content)
            elif cate == "成语谜面":
                cymm.append(content)

        if len(cyjs) != len(cys):
            cyjs.append("")
        if len(dgcc) != len(cys):
            dgcc.append("")
        if len(jyc) != len(cys):
            jyc.append("")
        if len(fyc) != len(cys):
            fyc.append("")
        if len(cycd) != len(cys):
            cycd.append("")
        if len(gqsc) != len(cys):
            gqsc.append("")
        if len(yfyf) != len(cys):
            yfyf.append("")
        if len(cyjg) != len(cys):
            cyjg.append("")
        if len(csnd) != len(cys):
            csnd.append("")
        if len(ywfy) != len(cys):
            ywfy.append("")
        if len(cymm) != len(cys):
            cymm.append("")

    data = {
        "成语": cys,
        "拼音": pys,
        "成语解释": cyjs,
        "典故出处": dgcc,
        "近义词": jyc,
        "反义词": fyc,
        "常用程度": cycd,
        "感情色彩": gqsc,
        "语法用法": yfyf,
        "成语结构": cyjg,
        "产生年代": csnd,
        "英文翻译": ywfy,
        "成语谜面": cymm
    }

    data = pd.DataFrame(data)
    data.to_csv("data/cycd.csv")


def is_chinese(string):
    flag = True
    for s in string:
        if s < u'\u4e00' or s > u'\u9fa5':
            flag = False
            break
    return flag


def merge():
    """
    以下是融合url1、url2和成语大全（31648个成语解释）.txt成语的结果
    :return:
    """
    data1 = pd.read_csv("data/cym1.csv")
    data2 = pd.read_csv("data/cym2.csv")
    data1 = data1["成语"].values.tolist()
    data2 = data2["成语"].values.tolist()
    # jiaoji = [i for i in data1 if i in data2]
    # only_in_data1 = [i for i in data1 if i not in data2]
    # only_in_data2 = [i for i in data2 if i not in data1]
    # print(only_in_data1)
    # print("=" * 100)
    # print(only_in_data2)
    data3 = cydq()
    data = list(set(data1 + data2 + data3))
    res = []
    for d in data:
        if is_chinese(d):
            res.append(d)
    with open('data/成语.txt', 'w', encoding='utf-8') as fp:
        fp.write("\n".join(res))


def cydq():
    res = []
    with codecs.open('data/成语大全（31648个成语解释）.txt', 'r', encoding="utf-8") as fp:
        data = fp.readlines()[:-1]
        for d in data:
            d = d.strip()
            if d:
                d = d.replace("  ", "")
                span = re.search("(.*?)拼音：", d)
                if span:
                    res.append(span.groups()[0])
    return res


if __name__ == '__main__':
    # get_all_chengyu1()
    # get_all_chengyu2()
    # cydq()
    # merge()

    # get_all_chengyu3()
    parse_url3_detail()