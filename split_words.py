import re
import requests
from urllib import error
from bs4 import BeautifulSoup
import os
import jieba.analyse
import requests

filename = 'result.txt'
num = 0
numPicture = 1
file = ''
List = []


def main():
    with open(filename) as file_object:
        lines = file_object.readlines()

    for line in lines:
        print(line.rstrip())
        seg_list = jieba.cut(line, cut_all=True)
        print("[]".join(seg_list))
        temp_w = 0
        temp_x = ""
        for x, w in jieba.analyse.extract_tags(line, withWeight=True):
            # print('%s %s' % (x, w))
            if w >= temp_w:
                temp_w = w
                temp_x = x
        print('本句关键词和权重： %s  %s' % (temp_x, temp_w))
        url = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=' + temp_x + '&pn='
        tot = Find(url)
        tmp = url
        t = 0
        while t < numPicture:
            try:
                url = tmp + str(t)
                result = requests.get(url, timeout=10)
                print(url)
            except error.HTTPError as e:
                print('网络错误，请调整网络后重试')
                t = t + 60
            else:
                dowmloadPicture(result.text,temp_x)
                t = t + 60


def Find(url):
    global List
    print('正在检测图片总数，请稍等.....')
    t = 0
    i = 1
    s = 0
    while t < 1000:
        Url = url + str(t)
        try:
            Resultimg = requests.get(Url, timeout=7)
        except BaseException:
            t = t + 60
            continue
        else:
            result = Resultimg.text
            pic_url = re.findall('"objURL":"(.*?)",', result, re.S)  # 先利用正则表达式找到图片url
            s += len(pic_url)
            if len(pic_url) == 0:
                break
            else:
                List.append(pic_url)
                t = t + 60
    return s




def dowmloadPicture(html, keyword):
    global num
    # t =0
    pic_url = re.findall('"objURL":"(.*?)",', html, re.S)  # 先利用正则表达式找到图片url
    print('找到关键词:' + keyword + '的图片，即将开始下载图片...')
    for each in pic_url:
        print('正在下载第' + str(num + 1) + '张图片，图片地址:' + str(each))
        try:
            if each is not None:
                pic = requests.get(each, timeout=7)
            else:
                continue
        except BaseException:
            print('错误，当前图片无法下载')
            continue
        else:
            string = 'image/' + r'\\' + str(num) + '.jpg'
            fp = open(string, 'wb')
            fp.write(pic.content)
            fp.close()
            num += 1
        if num >= numPicture:
            return


if __name__ == '__main__':
    main()
