# -*- coding: utf-8 -*-
from urllib.parse import urljoin

import scrapy
from scrapy.http import Request
import hashlib
from ArticleSpider.items import JobboleArticleItem,MyItemLoader



class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts']

    def parse(self, response):
        content_list = response.css('div[id=archive] div.floated-thumb div.post-thumb a')
        for node in content_list:
            url = node.css(' ::attr(href)').extract_first()
            img_url = node.css('img::attr(src)').extract_first()
            print(urljoin(response.url, url=url))
            yield Request(urljoin(response.url, url=url), meta={"front_img_url": img_url}, callback=self.parse_detail)
        next_url = response.css('.next.page-numbers::attr(href)').extract_first()
        if next_url:
            yield Request(urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self, response):
        # title = response.css('div.entry-header h1::text').extract_first()
        # create_date = response.css('p.entry-meta-hide-on-mobile::text').extract_first().replace('·', '').strip()
        # tags = response.css('p.entry-meta-hide-on-mobile a::text').extract()
        # tags = [tag for tag in tags if not tag.strip().endswith('评论')]
        # tag = '.'.join(tags)
        #
        # if response.css('div.post-adds span h10::text').extract_first():
        #     vote_num = int(response.css('div.post-adds span h10::text').extract_first())
        # else:
        #     vote_num = 0
        # collect_num = response.css('div.post-adds span.bookmark-btn::text').extract_first()
        # if re.match('.*(\d+).*', collect_num):
        #     collect_num = re.match('.*(\d+).*', collect_num).group(1)
        # else:
        #     collect_num = 0
        #
        # comment_num = response.css('a[href="#article-comment"] span::text').extract_first()
        # if re.match('.*(\d+).*', comment_num):
        #     comment_num = re.match('.*(\d+).*', comment_num).group(1)
        # else:
        #     comment_num = 0
        # content = response.css('div.entry').extract_first()
        # item = JobboleArticleItem()
        # item["title"] = title
        # try:
        #     create_date = datetime.datetime.strftime(create_date, '%Y-%m-%d')
        # except Exception as e:
        #     create_date = datetime.datetime.now().date()
        # item["create_date"] = create_date
        # item["url"] = response.url
        # item["url_id"] = hashlib.md5(response.url.encode(encoding='utf-8')).hexdigest()
        # item["tag"] = tag
        # item["vote_num"] = vote_num
        # item["collect_num"] = collect_num
        # item["comment_num"] = comment_num
        # item["content"] = content
        # item["front_image_url"] = [img_url]
        img_url = response.meta.get("front_img_url")
        item_loader = MyItemLoader(item=JobboleArticleItem(), response=response)
        item_loader.add_css("create_date", "p.entry-meta-hide-on-mobile::text")
        item_loader.add_css("title", "div.entry-header h1::text")
        item_loader.add_css("tag", "p.entry-meta-hide-on-mobile a::text")
        item_loader.add_css("vote_num", "div.post-adds span h10::text")
        item_loader.add_css("collect_num", "div.post-adds span.bookmark-btn::text")
        item_loader.add_css("comment_num", 'a[href="#article-comment"] span::text')
        item_loader.add_css("content", "div.entry")
        item_loader.add_value("front_image_url", [img_url])
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_id", hashlib.md5(response.url.encode(encoding='utf-8')).hexdigest())
        item = item_loader.load_item()

        yield item
        pass
