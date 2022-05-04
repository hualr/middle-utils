from pymongo import MongoClient

myclient = MongoClient(
    host='101.201.67.114',
    username='admin',
    password='123456',
    authSource='admin')
mydb = myclient['soar']
my_collection = mydb['book']

my_query = {"name": "Taobao"}

my_collection.delete_one(my_query)  # 删除一条数据

# 删除后输出
for x in my_collection.find():
    print(x)

my_query = {"name": {"$regex": "^F"}}

x = my_collection.delete_many(my_query)
print('删除name中以F开头的所有数据')
print(x.deleted_count, "个文档已删除")

# print('删除所有文档')
# x = mycol.delete_many({})
# print(x.deleted_count, "个文档已删除")
#
# print('删除所有集合')
# mycol.drop()
