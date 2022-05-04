import pymongo

myclient = pymongo.MongoClient(host='101.201.67.114',
                               username='admin',
                               password='123456',
                               authSource='admin')

mydb = myclient['soar']
my_collection = mydb['book']
print('查找一条数据' + '*' * 100)
x = my_collection.find_one()
print(x)
print('查找所有数据' + '*' * 100)
# y = mycol.find()  # 查找所有数据，返回一个对象
# print(y)
for y in my_collection.find():  # 输出所有数据
    print(y)

# 根据条件查询数据
myquery = {"name": "RUNOOB"}
mydoc = my_collection.find(myquery)
print('根据条件查询数据' + '*' * 100)
for x in mydoc:
    print(x)

# 读取 name 字段中第一个字母 ASCII 值大于 "H" 的数据，大于的修饰符条件为 {"$gt": "H"} :
myquery = {"name": {"$gt": "H"}}
mydoc = my_collection.find(myquery)
print('读取 name 字段中第一个字母 ASCII 值大于 "H" 的数据' + '*' * 100)
for x in mydoc:
    print(x)

# 以正则表达式来查询
myquery = {"name": {"$regex": "^R"}}  # name以R开头
mydoc = my_collection.find(myquery)
print('以正则表达式来查询' + '*' * 100)
for x in mydoc:
    print(x)

# 返回指定条数据
myresult = my_collection.find().limit(3)
print('只返回3条数据' + '*' * 100)
# 输出结果
for x in myresult:
    print(x)

# 查询指定字段的数据，设置为0则不查找，设置为1则查找，但如果没有指定id的数据，则无视'_id':0
print('查找字段为name,alexa的所有数据' + '*' * 100)
for z in my_collection.find(
        {}, {'_id': 0, 'name': 1, 'alexa': 1}):  # 查找字段为name,alexa的所有数据
    print(x)
print('*' * 100)
# 如果你设置了一个字段为0，则其他都为1，反之亦然。
for x in my_collection.find({}, {"alexa": 0}):
    print(x)

# for x in mycol.find({}, {"name": 1, "alexa": 0}): #  同时指定0和1则会报错
#   print(x)
