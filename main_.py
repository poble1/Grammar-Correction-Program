# -*- coding: utf-8 -*-
from pymongo import MongoClient
import requests
import sys

import KokomaQuever7 as koko
import Komoran3que2 as komo


#동사 격틀사전 탐색
def ckVerbDic(infinResult):
    client = MongoClient("localhost", 27017)
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


#'시' 유무 판단
def ckInfin(infinResult):
    tag = 0
    for k in infinResult:
        if k == "시":
            tag = 1
            print("'시'탐지")
    return tag




def main( ):
    init = []

    while(1):
        qu = input("문장을 입력하세요 : ")

        #꼬꼬마 실행
        infinResult = koko.callKokoma(qu)
        komoranResult = komo.callKomoran(qu)

        if infinResult == "-1": #만약 높임 표현이 아니면
            infinResult = komoranResult  #코모란 실행

        # 만약 원형에 '시'가 있으면
        if ckInfin(infinResult) == 1:
            #코모란 실행
            infinResult = komoranResult

        # 만약 격틀사전에 없다면
        ckhuman = []
        if ckVerbDic(infinResult) == -1:
            infinResult = komoranResult
        else:
            ckhuman = ckVerbDic(infinResult)

        print("원형 : " + infinResult)
        print("array:", ckhuman)

        #주어 탐색
        nsubj = dp.findNSUBJ(qu)
        print("주어", nsubj)

if __name__ == "__main__":
    main()
