#coding:gbk
#������Ӱ���صĴ������ӻ�������
#author:lzy

import re
import sys
import urllib
import urllib2

reload(sys)
sys.setdefaultencoding( "utf-8" )

type = sys.getfilesystemencoding()
_page = 1
movie_type = '''    ������Ӱ ---- 1
    ��̨��Ӱ ---- 2
    ŷ����Ӱ ---- 3
    �պ���Ӱ ---- 4
    �����Ӱ ---- 5
    ������Ӱ ---- 6'''
enter_type = '''  ������һ�� ---- b or back
  �˳�      ---- q or quit'''


def find_url():
    global _page
    sort_id = 1
    while True:
        print movie_type
        sort_id = raw_input("  �������Ӱ���Ͷ�Ӧ����ţ�")
        try:
            sort_id = int(sort_id)
          #  break
        except:
            print "��������룬����"
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
            input_num = raw_input(" ��������ѡ��ĵ�Ӱ��Ӧ�����(��һҳ��������n or next): ")
            if input_num in ['n','next']:
                _page += 1
                continue
            show_php = items[int(input_num)-1][0]
            find_pip(show_php)
            print enter_type
            enter_key = raw_input("��ѡ��")
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
    print " ���������ǣ�http://www.mp4ba.com/"+str(items_pip[0][0])
    print "  ����������: "+str(items_pip[0][1])
find_url()