import os

import datetime

import re
import scrapy
import sys

from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join


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
        return  ""
    else:
        return value
# 获取数字
def get_num(value):
    match_re = re.match('.*?(\d+).*', value[0])
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

    pass

#
# class DjangoArticleItem(DjangoItem):
#     article=models.ArticleModel()
