from scrapy.cmdline import execute
import os, sys
import MySQLdb
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", "jobbole"])
# coon=MySQLdb.connect(host='45.78.77.47',user='root',passwd='123456',db='article',charset='utf8',use_unicode=True)


