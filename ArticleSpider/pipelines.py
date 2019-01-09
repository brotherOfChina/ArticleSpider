# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs

from scrapy.exporters import JsonItemExporter
from scrapy.pipelines.images import ImagesPipeline
import MySQLdb
import MySQLdb.cursors

#
from twisted.enterprise import adbapi


class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item


# 保存图片
class ArticleFrontImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        if "front_img_path" in item:
            image_file_path = ""
            for ok, value in results:
                image_file_path = value["path"]
            item["front_img_path"] = image_file_path
        return item


# 自定义保存josn
class ArticleJsonPipeline(object):
    def __init__(self):
        self.file = open('article.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self):
        # 停止导出
        self.exporter.finish_exporting()
        self.close_spider()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
class MysqlPipeline1(object):
    def __init__(self):
        self.conn = MySQLdb.connect(host='45.78.77.47', user='root', passwd='123456', db='article', charset='utf8',
                               use_unicode=True)
        self.cursor=self.conn.cursor()


    def process_item(self, item, spider):
        insert_sql = """
                    insert into jobbole_article (title,url,url_id)
                    VALUES (%s,%s,%s)
                """
        self.cursor.execute(insert_sql, (
            item["title"], item["url"],item["url_id"]))
        self.conn.commit()
        return item

class MysqlPipeline(object):
    def __init__(self, ddPool):
        self.dbpool = ddPool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error,item,spider)
        return item
    #     处理异常
    def handle_error(self, failure,item,spider):
        print("错误11")
        print(failure)

    def do_insert(self, cursor, item):
        sql,params=item.get_insert_sql()
        cursor.execute(sql,params)
class DjangoPipeline(object):
    def process_item(self, item, spider):
        item.save()
        return item