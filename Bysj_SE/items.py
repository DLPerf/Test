# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from Bysj_SE.models.es_types import ArticleType
import redis


from elasticsearch_dsl.connections import connections
es = connections.create_connection(ArticleType._doc_type.using)

redis_cli = redis.StrictRedis()

def gen_suggest(index, info_tuple):
    #  根据字符串生成搜索建议数组
    used_words = set()
    suggests = []
    for text, weight in info_tuple:
        if text:
            #  调用es的analyze接口分析字符串
            words = es.indices.analyze(index= index,analyzer= "ik_max_word", params={"filter":["lowercase"]}, body= text)
            analyzed_words = set(r["token"] for r in words["tokens"] if len(r["token"])>1)
            new_words = analyzed_words - used_words
        else:
            new_words = set()

        if new_words:
            suggests.append({"input":list(new_words), "weight":weight})
    return suggests


class BysjSeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    href = scrapy.Field()
    article = scrapy.Field()
    date_time = scrapy.Field()
    comment = scrapy.Field()
    look = scrapy.Field()

class HaichuanItem(scrapy.Item):
    print("已经启动了HaichuanItem的处理器-1！！！")
    title = scrapy.Field()
    href = scrapy.Field()
    article = scrapy.Field()  #  文章内容
    date_time = scrapy.Field()  #  日期
    reply = scrapy.Field()  #  回复数量
    check = scrapy.Field()   #  查看数

    def save_to_es(self):
        article = ArticleType()
        article.reply = self['reply']
        article.article = self['article']
        article.date_time = self['date_time']
        article.check = self['check']
        article.title = self['title']
        article.href = self['href']
        #  生成搜索建议池
        article.suggest =  gen_suggest(ArticleType._doc_type.index,((article.title,10),(article.article,5)))
        article.save()

        redis_cli.incr("haichuan_count")
        return