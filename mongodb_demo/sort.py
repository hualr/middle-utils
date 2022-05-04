import pymongo

myclient = pymongo.MongoClient(host='101.201.67.114', username='admin', password='123456', authSource='admin')
mydb = myclient['soar']
my_collection = mydb['book']
print('对字段 alexa 按升序排序：')
mydoc = my_collection.find().sort("alexa")
for x in mydoc:
    print(x)

print('对字段 alexa 按降序排序：')
mydoc = my_collection.find().sort("alexa", -1)

for x in mydoc:
    print(x)
