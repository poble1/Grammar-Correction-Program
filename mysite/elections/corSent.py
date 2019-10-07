# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponseRedirect
from konlpy.tag import Kkma

# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

def ckSent(isrightVerb, ishumanNoun):
### 변형 부분 ###
    if isrightVerb == 1 and ishumanNoun == 1:
        right = "올바른 표현입니다."
        print(right)
        return 1
    elif ishumanNoun == 0:
        right = "올바른 표현입니다."
        print(right)
        return 1

    # 범주 찾기
    # elif ishumanNoun == -1 and ishumanNoun == -1:
    #     right = "올바른 표현입니다."
    #     print(right)
    #     return 1

    else:
        wrong = "올바르지 못한 표현입니다."
        print(wrong)
        return -1

def cgSent(sent, root, cls):
    print("st3t")
    tokens = sent.split(" ")
    answer = ""
    cgverb =""
    for token in tokens:
        if token == root+cls:
            answer = answer + ' ' +cgverb
        else:
            answer = answer + ' ' + token
    print("sas")
    return answer[1:]

def cgVerb(arr):
    que = []
    # 선어말 어미
    EP = ["EPH", "EPT", "EPP"]
    # 종결어미
    EF = ['EFN', 'EFQ', 'EFO', 'EFA', 'EFI', 'EFR']
    EC = ['ECD', 'ECE']

    # 마침표
    S = ["SF", "SP", "SS", "SE", "SO", "SW"]
    # 용언
    V = ["VV", "VA", "VXV", "VXA", "VCP"]  # "VCP" : 이다 -ex부부이다 와 같이 이다 가 원형인 경우 생각해야함
    VCP = ["이"]
    # XSV : 동사 파생형 접미사

    # 접미사
    X = ["XSN", "XSV", "XSA"]
    N = ["NNG", "NNP"]

    xtoken = []
    for token2 in arr:
        if que:
            if que[-1][1] in N: #큐의 마지막 값이 명사인데
                if token2[1] in V:
                    print("V입력")
                elif token2[1] in X:
                    print("X입력")
                elif token2[1] in N:
                    print("N입력")
                else:
                    #print("큐초기화")
                    que = []

        if token2[1] in N:
            if not que:  # 만약 큐에 아무것도 없으면
                que.append(token2)
            else:
                if que[-1][1] in N:  # 만약 앞에 명사가 있으면(복합명사)
                    que.append(token2)
                else:  # 명사 앞에 그 이외의 값이면
                    que = []  # 배열 초기화
                    que.append(token2)

        elif token2[1] in V and token2[0] not in VXV:
            #print(token2[1])
            if que:
                if que[-1][1] in N or que[-1][1] in "EF":  # 동사 앞의 값은 명사, EF만 올 수 있다.
                    que.append(token2)

                elif que[-1][1] == "XSN" and que[-1][0] == '화':  # XSN : (명사)화 시키다
                    if len(que) >= 2:
                        if que[-2][1] in N:
                            que.append(token2)
                        else:
                            que = []
                #만약 "이"가 나왔을 경우 큐에 동사가있으면 동작X
                elif token2[1] == "VCP" and token2[0] in VCP:
                    if que[-1][1] in V or que[-1][1] == "XSV": #마감하(실것)이(다)에서 이를 빼줌
                        continue

                ##없어 ->없어 다 때문에 고침
                elif que[-1][1] == "EC" or que[-1][1] == 'ECD':
                    if que[-1][0] not in ECD:
                        que.append(token2)
                    else:
                        continue

                elif token2[1] == "VA" and token2[0] in VA:
                    if que[-1][1] in V: #않 부정사가 나왔을때 큐에 값이 있으면
                        continue
                    else:
                        que.append(token2)

                else:  # 만약 큐에 이상한 값 들어있으면
                    que = []
                    que.append(token2)

            else: #큐에 아무것도 없을 경우
                que.append(token2)

        elif token2[1] in X: #마감 하 +이
            if que:
                if que[-1][1] in N:
                    que.append(token2)
                else:
                    #print("큐초기화2")
                    que = []
            else:
                que.append(token2)

        #print(que)
    result = ""
    twistSentVerb = ""

    if que:
        for k in que:
            result = result +k[0]
        result = result + '다'
    if arr[-1][1] in S:
        cls = arr[-1][0]

    return result
