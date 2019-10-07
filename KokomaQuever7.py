# -*- coding: utf-8 -*-

from konlpy.tag import Kkma
from konlpy.utils import pprint
kkma = Kkma()

#선어말 어미
EP = ["EPH", "EPT", "EPP"]
#종결어미
EF = ['EFN', 'EFQ', 'EFO', 'EFA', 'EFI', 'EFR']
EC = ['ECD', 'ECE']

#마침표
S = ["SF", "SP", "SS", "SE", "SO", "SW"]
#용언
V = ["VV", "VA", "VXV", "VXA", "VCP"]   #"VCP" : 이다 -ex부부이다 와 같이 이다 가 원형인 경우 생각해야함
VCP = ["이"]
#XSV : 동사 파생형 접미사

#접미사
X = ["XSN", "XSV", "XSA"]
N = ["NNG", "NNP"]

#용언 복원시 필요없는것
ECD = ["으니까요", "지", "니까요", "니", "어", "아"]
VXV = ["않"]
VA = ["않", "없"]

#겹문장
twistSentVerbQue = []
twistSentVerbArr = []

def callKokoma(qu):
    print("(꼬꼬마)형태소 분석중..")
    arr = kkma.pos(qu)
    print("형태소 분석 완료.")

    #동사가 높임말인지 검사
    if ckUpper(arr) == -1: #높임말이 아니면
        return "-1"

    # 동사 원형
    infinResult = ""
    infinResult = infinVerb(arr)

    # print("겹문장 : ", twistSentVerbArr)
    return infinResult

#동사 원형 복원
def infinVerb(arr):

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
            elif que[-1][1] == 'ECE' and que[-1][0] == '고':
                if token2[1] == "SP" and token2[0] == ",":
                    twistSentVerbQue.append([que[:-1]]) #'고'를 뺀 값 넣음
                    que = []
                    #("겹문장 인식")
                    #print(twistSentVerbQue)


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
        elif token2[1] in EC and token2[0] not in ECD:
            if que:
                if que[-1][1] in V:
                    que.append(token2)
                else:
                    #print("큐초기화3")
                    que = []
        #print(que)
    result = ""
    twistSentVerb = ""

    if que:
        for k in que:
            result = result +k[0]
        result = result + '다'
    twistVerb()
    return result

#겹문장의 동사를 추출
def twistVerb():
    if twistSentVerbQue:
        for TSVArr in twistSentVerbQue:
            temp = ""
            for l in TSVArr:
                temp = temp + l[0][0]
            twistSentVerbArr.append(temp + '다')


def ckUpper(arr):
    for token in arr:
        #print(token)
        if token[1] == "EPH":
            return 1 #높임말
    return -1 #높임말 아님



def chUptoLow(arr, upindx):
    sent = ""
    for token2 in arr:
        if arr.index(token2) != upindx:
            sent = sent + token2[0]
    print("\n**낮춤말로 변환**\n"+sent)


