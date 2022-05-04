import pymongo

myclient = pymongo.MongoClient(host='101.201.67.114', username='admin', password='123456', authSource='admin')
mydb = myclient['soar']
my_collection = mydb['book']

myquery = {"alexa": 1000}
newvalues = {"$set": {"alexa": 12345}}

my_collection.update_one(myquery, newvalues)  # 修改第一条查到的数据

# 输出修改后的  "sites"  集合
for x in my_collection.find():
    print(x)

x = my_collection.update_many({"name": {"$regex": "^F"}}, {"$set": {"alexa": "123"}})
print('查找所有以 F 开头的 name 字段，并将匹配到所有记录的 alexa 字段修改为 123：')
print(x.modified_count, "文档已修改")

for x in my_collection.find():
    print(x)
