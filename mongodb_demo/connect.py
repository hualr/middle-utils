# !/usr/bin/python3
# 安装：pip install pymongo

import pymongo

myclient = pymongo.MongoClient(
    host='101.201.67.114',
    username='admin',
    password='123456',
    authSource='admin')

# 注意: 在 MongoDB 中，数据库只有在内容插入后才会创建! 就是说，数据库创建后要创建集合(数据表)并插入一个文档(记录)，数据库才会真正创建。
# 读取 MongoDB 中的所有数据库，并判断指定的数据库是否存在：
dblist = myclient.list_database_names()
print(dblist)

mydb = myclient["soar"]
collist = mydb.list_collection_names()
print(collist)
