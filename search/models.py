from django.db import models

# Create your models here.

from elasticsearch_dsl import DocType,Date,Nested,Boolean,analyzer,Completion,Keyword,Text,Integer,InnerObjectWrapper

from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer

from elasticsearch_dsl.connections import connections
connections.create_connection(hosts=["localhost"]) # 设置连接服务器,允许连接多个服务器


# 自定义分析器
class CustomAnalyzer(_CustomAnalyzer):
    def get_analysis_definition(self):
        return {}

ik_analyzer = CustomAnalyzer('ik_max_word',filter=['lowercase']) # filter，大小写转换

class ArticleType(DocType):
    #伯乐在线文章类型
    suggest = Completion(analyzer=ik_analyzer)
    title = Text(analyzer="ik_max_word") #定义存储类型,分析器
    create_date = Date()
    url = Keyword() # 文章链接
    url_object_id = Keyword() # md5后链接
    front_image_url = Keyword() # 图片链接
    front_image_path = Keyword() # 图片存放路径
    praise_number = Integer()
    fav_nums = Integer()
    comment_nums = Integer()
    tags = Text(analyzer="ik_max_word")
    content = Text(analyzer="ik_max_word")
    
    class Meta:
        index = "jobbole" # 设置index名
        doc_type = "article" # 设置表名


if __name__ == "__main__":
    ArticleType.init()