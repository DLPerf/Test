from django.shortcuts import render
from django.views.generic.base import View
from search.models import ArticleType
from  django.http import HttpResponse
import json
from datetime import datetime
from elasticsearch import Elasticsearch   #  elasticse_dsl 是对elasticsearch的封装，elasticsearch是更底层的接口
import redis
import re
import request as rs
import subprocess
from Bysj_SE.models.es_types import ArticleType
import time


client = Elasticsearch(hosts=["127.0.0.1"])
redis_cli = redis.StrictRedis()

spider_signal = 0


class IndexView(View):
    #首页
    def get(self, request):
        topn_search = redis_cli.zrevrangebyscore("search_keywords_set", "+inf", "-inf", start=0, num=5)
        my_top_search = []
        for i in topn_search:
            my_top_search.append(str(i, encoding="utf-8"))
        return render(request, "index.html", {"topn_search":my_top_search})


# Create your views here.
class SearchSuggest(View):
    def get(self, request):
        key_words = request.GET.get('s','')

        re_datas = []

        if key_words:
            s = ArticleType.search()
            s = s.suggest('my_suggest',key_words, completion= {
                "field":"suggest",
                "fuzzy":{
                    "fuzziness":2
                },
                "size": 10
            })
            suggestions = s.execute_suggest()
            for match in suggestions.my_suggest[0].options:
                source = match._source
                re_datas.append(source['title'])
            return HttpResponse(json.dumps(re_datas),content_type='application/json')

class SearchView(View):
    def get(self,request):
        #  搜索词
        key_words = request.GET.get("q","")

        #  热门搜索
        redis_cli.zincrby("search_keywords_set", 1, key_words)
        topn_search = redis_cli.zrevrangebyscore("search_keywords_set", "+inf", "-inf", start=0, num=5)

        #  得到的是字节类型串，需要修改
        my_top_search = []
        for i in topn_search:
            my_top_search.append(str(i, encoding="utf-8"))

        page = request.GET.get("p","1")
        try:
            page = int(page)
        except:
            page = 1

        start_time =   datetime.now()
        haichuan_count = int(str(redis_cli.get("haichuan_count"), encoding="utf-8"))
        print("开始爬取数据了")
        #  读取 scrapy_pid.txt 看是否已经存在爬虫进程
        f = open('scrapy_pid.txt',"a+")
        k = open('key_words.txt',"a+")
        f.seek(0)
        s_pid = f.read()

        if s_pid == '':
            self.subProcessSpider(f,k,key_words)
        else:
            k.seek(0)
            if k.read() == key_words:
                pass
            else:
                subprocess.Popen('taskkill /f /pid {}'.format(int(s_pid)))
                f.truncate(0)
                self.subProcessSpider(f,k,key_words)

        f.close()
        k.close()

        response = client.search(
            index="haichuan",
            body={
                "query":{
                    "multi_match":{
                        "query":key_words,
                        "fields":["title","article"]
                    }
                },
                "from":(page - 1)*10,
                "size": 10,
                "highlight":{
                    "pre_tags": ['<span class="keyWord">'],
                    "post_tags": ["</span>"],
                    "fields":{
                        "title":{},
                        "article":{},
                    }
                }
            }
        )


        total_nums = response["hits"]["total"]
        if(page%10) > 0:
            page_nums = int(total_nums/10) + 1
        else:
            page_nums = int(total_nums/10)
        hit_list = []

        hit_list = self.get_hit_list(response)
        entity_link = ""
        best_first_item = hit_list[0]
        best_first_text = ""
        best_first_title=""
        if page == 1:
            #  得到keywords的实体链接信息
            url_1 = "http://shuyantech.com/api/cndbpedia/avpair?q=%s" % key_words
            entity_link = self.get_desc_words(self.get_text(url_1),0)

            # response_for_best = response["hits"]["hits"][0]["_source"]["article"]
            response_for_best = best_first_item["article"]
            dr = re.compile(r'<[^>]+>',re.S)
            response_for_best = dr.sub('', response_for_best)
            best_first_text = self.get_desc_words(response_for_best,1)
            best_first_title = dr.sub('',best_first_item["title"])
            print(response_for_best)

        end_time = datetime.now()
        last_seconds = (end_time - start_time).total_seconds()
        return render(request,"result.html",{
            "page":page,   #  页码
            "all_hits":hit_list,  #  搜索结果列表
            "key_words":key_words, #  搜索关键词
            "total_nums":total_nums,  #  搜索结果总数
            "page_nums":page_nums, #  页数
            "last_seconds":last_seconds,  #  搜索时间
            "topn_search": my_top_search,  #  搜索热门
            "haichuan_count":haichuan_count,    #  数据库共有多少条数据
            "entity_link": entity_link,  #  搜索实体结果
            "best_first_title":best_first_title,  #  分数最高的结果
            "best_first_href":best_first_item["href"],  #  分数最高的链接
            "best_first_text":best_first_text  #  对分数最高的结果进行分析
        }
                      )

    def get_text(self,url):
        rsbons = rs.get(url)
        entity_link = ""
        json_content = json.loads(rsbons.text)
        for i in json_content['ret']:
            if i[0] == "DESC":
                entity_link = i[1].replace("\n", "")
        return entity_link

    def get_desc_words(self,entity_link,search_type):
        if entity_link:
            entity_understand_url = "http://shuyantech.com/api/entitylinking/cutsegment?q=%s" % entity_link
            res_entity_understand = rs.get(entity_understand_url)
            res_entity_understand_json = json.loads(res_entity_understand.text)

            entity_link_list = list(entity_link)
            for entity_item in reversed(res_entity_understand_json["entities"]):
                cur_entity = entity_link[entity_item[0][0] : entity_item[0][1]]
                entity_link_list.insert(entity_item[0][1],"</a>")
                if search_type == 0:
                    entity_link_list.insert(entity_item[0][0],'<a href="http://kw.fudan.edu.cn/cndbpedia/search/?mention=%s&entity=%s" target="_blank">' % (cur_entity,cur_entity))
                else:
                    entity_link_list.insert(entity_item[0][0],'<a href="/search/?q=%s" target="_blank">' % cur_entity)
                entity_link = "".join(entity_link_list)
        return entity_link


    def get_hit_list(self, response):
        hit_list = []
        for hit in response["hits"]["hits"]:
            hit_dict = {}
            if "title" in hit["highlight"]:
                hit_dict["title"] = "".join(hit["highlight"]["title"])
            else:
                hit_dict["title"] = hit["_source"]["title"]
            if "article" in hit["highlight"]:
                hit_dict["article"] = "".join(hit["highlight"]["article"])[:500]
            else:
                hit_dict["article"] = hit["_source"]["article"][:500]

            hit_dict["date_time"] = hit["_source"]["date_time"]

            hit_dict["href"] = hit["_source"]["href"]
            hit_dict["score"] = hit["_score"]
            hit_list.append(hit_dict)
        return hit_list

    def get_best_text(self,response):
        return response["hits"]["hits"][0]["_source"]["article"]


    def subProcessSpider(self,f,k,key_words):
        ArticleType.init()
        p = subprocess.Popen('scrapy crawl Haichuan')
        f.write(str(p.pid))
        k.truncate(0)  # 先删除之前的搜索
        k.write(key_words)
        # time.sleep(60)

