# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponseRedirect
from konlpy.tag import Kkma

# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import re

def ckSent(isrightVerb, ishumanNoun, upperflag):
### 변형 부분 ###

    if ishumanNoun == -1:
        if upperflag == 1:
            right = "사물-높임말 틀린 표현입니다."
            print(right)
            return -1
        elif upperflag == -1:
            right = "사물-낮춤말 옳은 표현입니다."
            print(right)
            return 1
    elif ishumanNoun == 0:
        if isrightVerb == 1 and upperflag == 1:
            right = "높임말 옳은 표현입니다."
            print(right)
            return 1
        elif isrightVerb == -1 and upperflag == 1:
            right = "잘못쓰이는 높임 표현입니다."
            print(right)
            return -1
    if isrightVerb == 1:
            if ishumanNoun == 1:
                right = "올바른 표현입니다."
                print(right)
                return 1
            elif ishumanNoun == 0:
                right = "올바른 표현입니다."
                print(right)
                return 1
    else:
        wrong = "올바르지 못한 표현입니다."
        print(wrong)
        return -1

def cgSent(sent, rowVerb):
    #print("st3t")
    tokens = sent.split(" ")
    answer = ""
    cgverb =""
    for token in tokens:
        if token == rowVerb:
            answer = answer
        else:
            answer = answer + ' ' + token
    #print("sas : ")
    return answer[1:]

def cgVerb(arr):
    # 선어말 어미
    EP = ["EPT", "EPP"]
    # 종결어미
    EF = ['EFN', 'EFQ', 'EFO', 'EFA', 'EFI', 'EFR']

    # 마침표
    S = ["SF", "SP", "SS", "SE", "SO", "SW"]
    # 용언
    V = ["VV", "VA", "VXV", "VXA", "VCP"]  # "VCP" : 이다 -ex부부이다 와 같이 이다 가 원형s인 경우 생각해야함
    VCP = ["이"]
    # XSV : 동사 파생형 접미사
    ECD = ["으니까요", "지", "니까요", "니", "어", "아"]
    VXV = ["않"]
    # 접미사
    X = ["XSN", "XSV", "XSA"]
    N = ["NNG", "NNP"]



    S = ['SF', 'SE', 'SS', 'SP', 'S0']
    que = []

    # 이전 단어 저장

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

            elif que[-1][1] in V or que[-1][1] in X or que[-1][1] in EP or que[-1][1] in EP:
                if not token2[1] == "EPH" and token2[0] not in ['시', '으시']:
                    que.append(token2)
                    continue

        if token2[1] in N:
            if not que:  # 만약 큐에 아무것도 없으면
                que.append(token2)
            else:
                if que[-1][1] in N:  # 만약 앞에 명사가 있으면(복합명사)
                    que.append(token2)
                else:  # 명사 앞에 그 이외의 값이면
                    que = []  # 배열 초기화
                    que.append(token2)

        elif token2[1] in X:
            que.append(token2)

        elif token2[1] in V:
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
                else:  # 만약 큐에 이상한 값 들어있으면
                    que = []
                    que.append(token2)

            else: #큐에 아무것도 없을 경우
                que.append(token2)


    result = ""
    if que:
        for k in que:
            result = result + k[0]

    result2 = ""
    i = 0
    JONGSUNG_LIST = [' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ',
                     'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
    JUNGSUNG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
    CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
    START_HANGLE = 44032
    exceptArr = ['오','하']
    exceptAns = ['왔', '했']

    atArr = ['았','었']

    while(i < len(result)):
        #print(result[i])
        if result[i] in atArr: #었,았
            cho = (ord(result[i-1]) - ord('가'))//588
            mid = ((ord(result[i-1]) - ord('가')) - (588*cho)) // 28
            jong = (ord(result[i-1]) - ord('가')) - (588*cho) - 28*mid
            print(result[i-1], jong, mid, cho)

            if jong == 0 and mid == JUNGSUNG_LIST.index('ㅣ'):
                temp = 44032 + (cho * 588) + (JUNGSUNG_LIST.index('ㅕ') * 28) + JONGSUNG_LIST.index('ㅆ')
                result2 = result2[:-1] + chr(temp)
                i = i+1
                continue
            elif jong == 0 and mid == JUNGSUNG_LIST.index('ㅏ'):
                temp = 44032 + (cho * 588) + (JUNGSUNG_LIST.index('ㅏ') * 28) + JONGSUNG_LIST.index('ㅆ')
                result2 = result2[:-1] + chr(temp)
                i = i+1
                continue
            elif result[i-1] in exceptArr:
                indextemp = exceptArr.index(result[i-1])
                result2 = result2[:-1] + exceptAns[indextemp]
                i = i + 1
                continue
        elif result[i] in JONGSUNG_LIST:
            cho = (ord(result[i-1]) - ord('가'))//588
            mid = ((ord(result[i-1]) - ord('가')) - (588*cho)) // 28
            jong = (ord(result[i-1]) - ord('가')) - (588*cho) - 28*mid
            if jong != 0 and result[i] == 'ㅂ':
                result2 = result2 + '습'
                i = i + 1
                continue
            else:
                temp = ord(result2[-1]) + JONGSUNG_LIST.index(result[i])
                result2 = result2[:-1] + chr(temp)
                i = i+1
                continue
        else:
            result2 = result2 + result[i]
            i = i+1
            continue

        result2 = result2 + result[i]
        i = i+1
    print(result2)
    return result2