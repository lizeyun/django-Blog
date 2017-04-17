----------> jango 初体验 搭建个人blog 和公司运维平台 <-------


$pip install django==1.8   #安装1.8版本django
$ln -s /usr/local/pyxxx/xxx/bin/*  /usr/bin/* #设置全局变量


$mkdir django -> cd django -> django-admin.py startproject lzzz  #开始项目
$tree 
	.
	└── lzzz
		├── lzzz
		│   ├── __init__.py    #初始化，模块导入
		│   ├── settings.py	   #配置文件
		│   ├── urls.py        #路由
		│   └── wsgi.py        不懂
		└── manage.py

	2 directories, 5 files  #项目结构
	
$mkdir templates --> mkdir static
$python manage.py migrate  #穿件sqllite3 简单数据库
$python manage.py makemigrations #初始化数据

##http://www.maiziedu.com/article/8547/  --> django 中引用CSS js 的方法

#django CSRF认证失败
 -->django 禁用CSRF 的方法：
			修改C:\Python27\Lib\site-packages\django\middleware\csrf.py
			#找到如下代码：
					if request.method not in ('GET', 'HEAD', 'OPTIONS', 'TRACE'): 
					#修改为：
					if request.method not in ('GET','POST', 'HEAD', 'OPTIONS', 'TRACE'):
					
#防止表单重新提交
		-->return redirect(r'/server')
		
#表单提交多选项时 一个key对应多个键值

	-->print request.POST["check_options"]
       a =  request.POST.getlist("check_options") #返回列表
		
		
models.py
1.抽象继承 ： 基类#class Meta:
								abstract = True
			  子类#class son_class(FatherClass):
				如果想要继承Meta属性#class Meta(FatherClass.Meta):
										
2.多表继承

				class Place(models.Model):
					name = models.CharField(max_length=50)
					address = models.CharField(max_length=80)
				 
				class Restaurant(Place):
					serves_hot_dogs = models.BooleanField()
					serves_pizza = models.BooleanField()
				Restaurant 通过创建 OneToOneField 来实现
			sql:BEGIN;
					CREATE TABLE "myapp_place" (
						"id" integer NOT NULL PRIMARY KEY,
						"name" varchar(50) NOT NULL,
						"address" varchar(80) NOT NULL
					)
					;
					CREATE TABLE "myapp_restaurant" (
						"place_ptr_id" integer NOT NULL PRIMARY KEY REFERENCES "myapp_place" ("id"),
					 
						"serves_hot_dogs" bool NOT NULL,
						"serves_pizza" bool NOT NULL
					)
					;

					{% for comment in comments %}
                        <div class="media">
                            <a class="pull-left" href="#">
                                <img class="media-object" src="/static/images/head.png" alt="">
                            </a>
                            <div class="media-body">
                            <h4 class="media-heading">{{ comment.username }}
                                <small>{{ comment.create_time  }}</small>
                            </h4>
                                {{ comment.content }}
                            </div>
                        </div>
                      {% endfor %}

















	
scrapy 存入Mysql 操作一览

1.setting.py --># start MySQL database configure setting
				MYSQL_HOST = 'localhost'
				MYSQL_DBNAME = 'cnblogsdb'
				MYSQL_USER = 'root'
				MYSQL_PASSWD = 'root'
				# end of MySQL database configure setting
				
2.pipeline 文件
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import copy
import MySQLdb
import MySQLdb.cursors


from scrapy import log
from twisted.enterprise import adbapi
from scrapy.http import Request



class CboooMysqlPipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
          #  host = '192.168.8.199',
            db = 'lzymovie',
            user = 'root',
            passwd = 'pixdb@01',
            cursorclass = MySQLdb.cursors.DictCursor,
            charset = 'utf8',
            use_unicode = False
        )
        
        
    def process_item(self, item, spider):
       # print spider
        #run db qurey in thread pool
        asynitem = copy.deepcopy(item)  #由于scrapy爬取网页和存入数据是异步进行的，所以存在冲突，deepcopy可以解决
        query = self.dbpool.runInteraction(self._conditional_insert, asynitem)
        query.addErrback(self.handle_error)
        return item
    
    def _conditional_insert(self, tx, item):
        tx.execute("select * from showing_movie where movie_name= %s",(item['movie_name'][0],))
        ret = tx.fetchone()

        if ret:
            #防止重复提交
            log.msg("Item already stored in db:%s" % item['movie_name'][0], level=log.DEBUG)
        else:
            tx.execute("insert into showing_movie (ranking, movie_name, area, percent, actor, director, length, total_box_office, current_box_office, pub_days, img_url)\
                values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (item['ranking'][0],
                 item['movie_name'][0],
                 item['area'][0],
                 item['percent'][0],
                 item['actor'][0],
                 item['director'][0],
                 item['length'][0],
                 item['total_box_office'][0],
                 item['current_box_office'][0],
                 item['pub_days'][0],
                 item['img_url'][0]))
        #print "Item stored in db: %s" % item
    def handle_error(self, e):
        print e

3. cat cbooo/settings.py #配置文件
# -*- coding: utf-8 -*-


BOT_NAME = 'cbooo'
SPIDER_MODULES = ['cbooo.spiders']
NEWSPIDER_MODULE = 'cbooo.spiders'
ITEM_PIPELINES={
    'cbooo.pipelines.CboooMysqlPipeline':100,
}
LOG_LEVEL='DEBUG'

DOWNLOAD_DELAY = 2
RANDOMIZE_DOWNLOAD_DELAY = True
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.54 Safari/536.5'
COOKIES_ENABLED = True



