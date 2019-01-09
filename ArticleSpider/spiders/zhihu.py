# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
import re
import json
import datetime
from scrapy.loader import ItemLoader
from ArticleSpider.items import ZhiHuAnswerItem,ZhihuQuestionItem


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/signup?next=%2F']
    start_answer_url="https://www.zhihu.com/api/v4/questions/{}/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit={}&offset={}&sort_by=default"
    headers = {
        "HOST": "www.zhihu.com",
        "Referer": "https://www.zhizhu.com",
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
    }

    def parse(self, response):
        print(response.url)
        all_urls = response.css('a::attr(href)').extract()
        all_urls = [parse.urljoin(response.url, url) for url in all_urls]
        all_urls = filter(lambda x: True if x.startswith("https") else False, all_urls)
        for url in all_urls:
            match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", url)
            if match_obj:
                request_url = match_obj.group(1)
                request_id = int(match_obj.group(2))
                yield scrapy.Request(request_url, headers=self.headers, callback=self.parse_question,meta={"request_id":request_id})
            else:
                yield scrapy.Request(url, headers=self.headers, callback=self.parse)

    def parse_question(self, response):
        item_loader = ItemLoader(item=ZhihuQuestionItem(), response=response)
        item_loader.add_css("title", "h1.QuestionHeader-title::text")
        item_loader.add_css('content', ".QuestionHeader-detail div span::text")

        item_loader.add_css("answer_num", ".List-headerText span::text")
        item_loader.add_css("comments_num", ".QuestionHeader-Comment button::text")
        item_loader.add_css("watch_user_num", ".QuestionFollowStatus-counts button div strong::text")
        item_loader.add_css("click_num", ".QuestionFollowStatus-counts div div strong::text")
        item_loader.add_css("topics", ".QuestionHeader-topics .Popover div::text")
        item_loader.add_value("url", response.url)

        request_id = response.meta.get("request_id")
        item_loader.add_value("zhihu_id", request_id)
        item_loader.add_value("crawl_time", datetime.datetime.now())
        question_item = item_loader.load_item()
        yield scrapy.Request(self.start_answer_url.format(request_id, 20,1),headers=self.headers,callback=self.parse_answer)
        yield question_item
    def parse_answer(self,response):
        answer_json=json.loads(response.text)
        is_end=answer_json["paging"]["is_end"]
        total_answers=answer_json["paging"]["totals"]
        next_url=answer_json["paging"]["next"]
        for answer in answer_json["data"]:
            answer_item=ZhiHuAnswerItem()
            answer_item["zhihu_id"]=answer["id"]
            answer_item["url"]=answer["url"]
            answer_item["question_id"]=answer["question"]["id"]
            answer_item["author_id"]=answer["author"]["id"] if "id" in answer["author"] else None
            answer_item["content"]=answer["content"] if "content" in answer else None
            answer_item["parise_num"]=answer["voteup_count"]
            answer_item["comments_num"]=answer["comment_count"]
            answer_item["create_time"]=answer["created_time"]
            answer_item["update_time"]=answer["updated_time"]
            answer_item["crawl_time"]=datetime.datetime.now()
            yield answer_item

        if not is_end:
            yield scrapy.Request(next_url, headers=self.headers,callback=self.parse_answer)




    def start_requests(self):
        from selenium import webdriver
        browser = webdriver.Chrome(executable_path="H:\python_work_space\project\ArticleSpider/tools\chromedriver.exe")

        browser.get("https://www.zhihu.com/signin")
        browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(
            "18404975605")
        browser.find_element_by_css_selector(".SignFlow-password input").send_keys(
            "5178019q.")
        browser.find_element_by_css_selector(
            ".Button.SignFlow-submitButton").click()
        import time
        time.sleep(10)
        Cookies = browser.get_cookies()
        print(Cookies)
        cookie_dict = {}
        import pickle
        for cookie in Cookies:
            # 写入文件
            # 此处大家修改一下自己文件的所在路径
            f = open(
                'H:\python_work_space\project\ArticleSpider\ArticleSpider\cookies\zhihu' + cookie['name'] + '.zhihu',
                'wb')
            pickle.dump(cookie, f)
            f.close()
            cookie_dict[cookie['name']] = cookie['value']
        browser.close()
        return [scrapy.Request('https://www.zhihu.com/#signin', headers=self.headers, cookies=cookie_dict,
                               callback=self.parse)]


