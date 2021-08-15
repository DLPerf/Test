# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from jieba import lcut

from gensim.similarities import SparseMatrixSimilarity
from gensim.corpora import Dictionary
from gensim.models import TfidfModel
import json
import pymysql
import grequests


class BysjSePipeline:

    # def __init__(self, data_base):
    #     self.data_base = data_base
    #     self.item_table = None

    # @classmethod
    # def from_crawler(cls, crawler):
    #     """
    #     创建对象用于读取文件
    #     :param crawler:
    #     :return:
    #     """
    #     #  去 setting.py 文件中找到相关配置参数
    #     data_base = crawler.settings.get('DB')
    #
    #     return cls(data_base)


    def open_spider(self, spider):
        self.item_table = open('new.json', 'a', encoding='utf-8')

        print('Data are being writed into file now.')


    def close_spider(self, spider):
        self.item_table.close()

        print('File is closed.')

    def process_item(self, item, spider):
        tpl = "%s\b\b\b\b%s\n" %(item['title'], item['href'])

        self.item_table.write(tpl)

        """       
         如果想要其他的pipline处理这里得到的数据，就在结尾 return item
         如果不想将item返回就抛出一个异常:
            from scrapy.exceptions import DropItem
            就在结尾 raise  DropItem()        
        """
        # return item
        raise DropItem()


class HaichuanPipeline():

    def __init__(self):
        self.item_table = open('haichuan02.json', 'w', encoding='utf-8')

    def open_spider(self, spider):
        self.db = pymysql.connect(host='localhost', user='root', passwd='root', port=3306, db='spiders')
        self.cursor = self.db.cursor()
        self.k = open('key_words.txt', "r")
        self.k.seek(0)
        print('Data are being writed into file now.')

    def close_spider(self, spider):
        self.db.close()
        self.k.close()
        print('File is closed.')

    def process_item(self, item, spider):
        #  这里应该添加主题相关性分析
        # # 文本集和搜索词
        # texts = [item['title'],item['article']]
        # keyword = '二氧化碳'
        # # 1、将【文本集】生成【分词列表】
        # texts = [lcut(text) for text in texts]
        # # 2、基于文本集建立【词典】，并获得词典特征数
        # dictionary = Dictionary(texts)
        # num_features = len(dictionary.token2id)
        # # 3.1、基于词典，将【分词列表集】转换成【稀疏向量集】，称作【语料库】
        # corpus = [dictionary.doc2bow(text) for text in texts]
        # # 3.2、同理，用【词典】把【搜索词】也转换为【稀疏向量】
        # kw_vector = dictionary.doc2bow(lcut(keyword))
        # # 4、创建【TF-IDF模型】，传入【语料库】来训练
        # tfidf = TfidfModel(corpus)
        # # 5、用训练好的【TF-IDF模型】处理【被检索文本】和【搜索词】
        # tf_texts = tfidf[corpus]  # 此处将【语料库】用作【被检索文本】
        # tf_kw = tfidf[kw_vector]
        # # 6、相似度计算
        # sparse_matrix = SparseMatrixSimilarity(tf_texts, num_features)
        # similarities = sparse_matrix.get_similarities(tf_kw)
        # #
        #
        # #  利用mysql对url去重
        #
        # # # print(item['title'], '---------->', item['article'])
        # for i in similarities:
        #     if i > 0:
        #         sql01 = 'CREATE TABLE IF NOT EXISTS SPIDER_URLS (url VARCHAR(255) NOT NULL, PRIMARY KEY(url))'
        #         self.cursor.execute(sql01)
        #         sql = 'INSERT INTO spider_urls(url) VALUES (%s)'
        #         try:
        #             if self.cursor.execute(sql, (item['href'])):
        #                 self.db.commit()
        #                 item.save_to_es()
        #         except:
        #             self.db.rollback()
        #         break

        item.save_to_es()

        #  读取文件匹配关键词
        # keyword = self.k.read()
        # sql01 = 'CREATE TABLE IF NOT EXISTS SPIDER_URLS (url VARCHAR(255) NOT NULL, PRIMARY KEY(url))'
        # if item['article'] == '':
        #     pass
        # else:
        #     total_text = item['title'] + "," + item['article']
        #     req_list = [
        #         grequests.get("http://shuyantech.com/api/entitylinking/cutsegment?q=%s" % total_text),
        #         grequests.get("http://shuyantech.com/api/entitylinking/cutsegment?q=%s" % keyword)
        #     ]
        #
        #     res_list = grequests.map(req_list)
        #     for i in res_list[0].text['cuts']:
        #         if i in res_list[1].text['cuts']:
        #             #############################################################################
        #             self.cursor.execute(sql01)
        #             sql = 'INSERT INTO spider_urls(url) VALUES (%s)'
        #             try:
        #                 if self.cursor.execute(sql, (item['href'])):
        #                     self.db.commit()
        #                     item.save_to_es()
        #             except:
        #                 self.db.rollback()
        #             #############################################################################



        return item