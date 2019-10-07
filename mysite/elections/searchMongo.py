from pymongo import MongoClient

client = MongoClient("localhost", 27017)
database = client.graDic


#동사 격틀사전 탐색
def ckNounbDic(subj):
    collection = database.NounDics
    collection2 = database.SenseDics
    tag = 0
    results = collection.find({"key": subj}, {"value": 1, '_id': 0})

    categorys = ["범주 없음"]
    
    ####################수정할부분############## 몽고디비에 없을때 처리
    for result in results:
        tests = result.values()
        for test in tests:
            categorys = test


    print("주어의 범주 : ", categorys)

    if categorys == ["범주 없음"]: #모두 가능
        return 0

    for category in categorys:
        results = collection2.find({"key": category}, {"value": 1, '_id': 0})
        for result in results:
            tests = result.values()
            for test in tests:
                if "인간" in test:
                    return 1
    return -1




#동사 격틀사전 탐색
def ckVerbDic(infinResult):
    database = client.graDic
    collection = database.verbDics
    tag = 0
    results = collection.find({"key": infinResult}, {"value": 1, '_id': 0})
    #print(results)

    ####################수정할부분##############
    for result in results:
        tests = result.values()
        for test in tests:
            return test
    print("격틀사전에 없음")
    return -1
