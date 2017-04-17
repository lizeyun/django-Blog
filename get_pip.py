#coding:gbk
#搜索电影下载的磁力链接或者种子
#author:lzy

import re
import sys
import urllib
import urllib2

reload(sys)
sys.setdefaultencoding( "utf-8" )

type = sys.getfilesystemencoding()
_page = 1
movie_type = '''    国产电影 ---- 1
    港台电影 ---- 2
    欧美电影 ---- 3
    日韩电影 ---- 4
    海外电影 ---- 5
    动画电影 ---- 6'''
enter_type = '''  返回上一层 ---- b or back
  退出      ---- q or quit'''


def find_url():
    global _page
    sort_id = 1
    while True:
        print movie_type
        sort_id = raw_input("  请输入电影类型对应的序号：")
        try:
            sort_id = int(sort_id)
          #  break
        except:
            print "错误的输入，重试"
            continue
        while True:
            url_address = "http://www.mp4ba.com/index.php?sort_id="+str(sort_id)+"&page="+str(_page)
            print url_address
            f = urllib2.urlopen(url_address,timeout=5)
            content = f.read().decode('utf-8').encode(type)
            pattern = re.compile('<a style=.*? href="(.*?)".*?>(.*?)</a>',re.S)
            items = re.findall(pattern,content)        
            for index,item in enumerate(items):
                    if "1080" in item[1]:
                        movie_name = item[1].replace("\r\n","").split(".")[0]
                        print index+1,movie_name
            input_num = raw_input(" 请输入你选择的电影对应的序号(下一页，请输入n or next): ")
            if input_num in ['n','next']:
                _page += 1
                continue
            show_php = items[int(input_num)-1][0]
            find_pip(show_php)
            print enter_type
            enter_key = raw_input("请选择：")
            if enter_key in ['q','quit']:
                sys.exit()
            if enter_key in ['b','back']:
                break
        
            
def find_pip(show_php):
    url_pip = "http://www.mp4ba.com/"+str(show_php)
    g = urllib2.urlopen(url_pip,timeout=5)
    content_pip = g.read().decode('utf-8').encode(type)
    pattern_pip = re.compile('id="download" href="(.*?)">.*?id="magnet" href="(.*?)"',re.S)
    items_pip = re.findall(pattern_pip,content_pip)
    print " 种子链接是：http://www.mp4ba.com/"+str(items_pip[0][0])
    print "  磁力链接是: "+str(items_pip[0][1])
find_url()