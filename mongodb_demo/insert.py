import pymongo

myclient = pymongo.MongoClient(
    host='101.201.67.114',
    username='admin',
    password='123456',
    authSource='admin')
mydb = myclient['soar']
my_collection = mydb['book']

my_dict = {'name': 'pr', 'alexa': 1000, 'url': 'http:www.baidu.com'}
x = my_collection.insert_one(my_dict)  # 插入一条数据
print(x)
print(x.inserted_id)  # 如果我们在插入文档时没有指定 _id，MongoDB 会为每个文档添加一个唯一的 id。

# 插入指定id
mylist = [
    {"_id": 1, "name": "RUNOOB", "cn_name": "菜鸟教程"},
    {"_id": 2, "name": "Google", "address": "Google 搜索"},
    {"_id": 3, "name": "Facebook", "address": "脸书"},
    {"_id": 4, "name": "Taobao", "address": "淘宝"},
    {"_id": 5, "name": "Zhihu", "address": "知乎"}
]
mylist2 = [
    {"name": "RUNOOB", "cn_name": "菜鸟教程"},
    {"name": "Google", "address": "Google 搜索"},
    {"name": "Facebook", "address": "脸书"},
    {"name": "Taobao", "address": "淘宝"},
    {"name": "Zhihu", "address": "知乎"}
]

many = my_collection.insert_many(mylist2, ordered=False)
print(x.inserted_ids)
