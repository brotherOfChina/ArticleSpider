import os

import datetime

import re
import scrapy
import sys

from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from ArticleSpider.myutils.common import extract_num,int2date
from ArticleSpider.settings import SQL_DATE_FORMAT,SQL_TIME_FORMAT
# class ArticleSpiderItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass
# 自定义loader
class MyItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


# 日期转换
def date_convert(value):
    try:
        create_date = datetime.datetime.strftime(value.replace('·', '').strip(), '%Y-%m-%d')
    except Exception as e:
        create_date = datetime.datetime.now().date()
    return create_date


# 添加
def add_jobbole(value):
    return value + 'bole'


def delete_comment_tags(value):
    if "评论" in value:
        return ""
    else:
        return value


# 从字符串获取数字
def get_num(value):
    match_re = re.match('.*?(\d+).*', value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0
    return nums


def handle_tag(value):
    tags = [tag for tag in value if not tag.strip().endswith('评论')]
    return '.'.join(tags)


def return_value(value):
    return value


class JobboleArticleItem(scrapy.Item):
    title = scrapy.Field(
        input_processor=MapCompose(lambda x: x + 'job', add_jobbole),
    )
    create_date = scrapy.Field(
        input_processor=MapCompose(date_convert),
    )
    tag = scrapy.Field(
        input_processor=MapCompose(delete_comment_tags),
        output_processor=Join(",")
    )
    url = scrapy.Field()
    url_id = scrapy.Field()
    vote_num = scrapy.Field(
        input_processor=MapCompose(get_num)
    )
    collect_num = scrapy.Field(
        input_processor=MapCompose(get_num)
    )
    comment_num = scrapy.Field(
        input_processor=MapCompose(get_num)
    )
    content = scrapy.Field()
    front_image_url = scrapy.Field(
        output_processor=MapCompose(return_value)
    )
    front_img_path = scrapy.Field()

    def get_insert_sql(self):
        inser_sql = """
                   insert into jobbole_article (title,url,create_date,tags,vote_num,collect_num,comment_num,content,front_image_url,url_id)
                   VALUES (%s,%s, % s, % s, % s, % s, % s, % s, % s,%s)
                   """
        params= (
            self["title"], self["url"], self["create_date"], self["tag"], self["vote_num"], self["collect_num"],
            self["comment_num"], self["content"], self["front_image_url"],self["url_id"])
        return inser_sql,params



#
# class DjangoArticleItem(DjangoItem):
#     article=models.ArticleModel()
class ZhihuQuestionItem(scrapy.Item):
    zhihu_id = scrapy.Field()
    topics = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    answer_num = scrapy.Field()
    comments_num = scrapy.Field()
    watch_user_num = scrapy.Field()
    click_num = scrapy.Field()
    crawl_time = scrapy.Field()
    crawl_update_time = scrapy.Field()
    def get_insert_sql(self):
        insert_sql="""
                 insert into zhihu_question (zhihu_id,topics,url,title,content,answer_num,comments_num,watch_user_num,click_num,crawl_time)
                 
                  
                   VALUES (%s,%s, %s, %s, %s, %s, %s,%s,%s,%s)
                   ON DUPLICATE KEY UPDATE  content=VALUES (content),comments_num=VALUES (comments_num) ,answer_num=VALUES (answer_num)
        """
        zhihu_id=int(self["zhihu_id"][0])
        topics=",".join(self["topics"])
        url=self["url"][0]
        title=self["title"][0]
        try:
            content = "".join(self["content"])
        except:
            content=""

        answer_num=extract_num(self["answer_num"][0])
        comments_num=extract_num(self["comments_num"][0])
        watch_user_num=extract_num(self["watch_user_num"][0])
        click_num=extract_num(self["click_num"][0])
        crawl_time=datetime.datetime.now().strftime(SQL_DATE_FORMAT)
        params=(zhihu_id,topics,url,title,content,answer_num,comments_num,watch_user_num,click_num,crawl_time)
        return insert_sql,params


class ZhiHuAnswerItem(scrapy.Item):
    zhihu_id = scrapy.Field()
    url = scrapy.Field()
    question_id = scrapy.Field()
    author_id = scrapy.Field()
    parise_num = scrapy.Field()
    comments_num = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()
    crawl_time = scrapy.Field()
    crawl_update_time = scrapy.Field()
    content = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                   insert into zhihu_answer (zhihu_id,url,question_id,author_id,parise_num,comments_num,create_time,update_time,crawl_time,content)
                    VALUES (%s,%s, %s, %s, %s, %s, %s,%s,%s,%s)
                    ON DUPLICATE KEY UPDATE content=VALUES (content),parise_num=VALUES (parise_num) ,comments_num=VALUES (comments_num),update_time=VALUES (update_time)
          """
        zhihu_id = self["zhihu_id"]
        url = self["url"]
        question_id = self["question_id"]
        author_id = str(self["author_id"])
        parise_num = self["parise_num"]
        comments_num =self["comments_num"]
        create_time =datetime.datetime.fromtimestamp(self["create_time"]).strftime(SQL_DATE_FORMAT)
        update_time =datetime.datetime.fromtimestamp(self["update_time"]).strftime(SQL_DATE_FORMAT)
        crawl_time =  datetime.datetime.now().strftime(SQL_DATE_FORMAT)
        content = self["content"]
        params = (zhihu_id, url, question_id, author_id, parise_num, comments_num, create_time, update_time, crawl_time, content)
        return insert_sql, params
    pass
