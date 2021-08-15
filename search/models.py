from django.db import models

# Create your models here.
from datetime import datetime

from elasticsearch_dsl import DocType, Date, Nested, Boolean, \
    analyzer, Completion, Keyword, Text, Integer

from elasticsearch_dsl.connections import connections

from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer


connections.create_connection(hosts= ["localhost"])


# Define a default Elasticsearch client
connections.create_connection(hosts=['localhost'])

class CustomAnalyzer(_CustomAnalyzer):
    def get_analysis_definition(self):
        return {}

ik_analyzer = CustomAnalyzer('ik_max_word',filter=['lowercase'])


class ArticleType(DocType):
    #  海川化工文章类型
    suggest = Completion(analyzer= ik_analyzer)
    title = Text(analyzer= "ik_max_word")
    date_time = Date()
    href = Keyword()
    article = Text(analyzer= "ik_max_word")
    reply = Integer()
    check = Integer()


    class Meta:
        index = "haichuan"
        doc_type = "article"

if __name__ == "__main__":
    ArticleType.init()