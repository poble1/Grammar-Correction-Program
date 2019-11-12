from konlpy.tag import Komoran
komoran = Komoran()

#선어말 어미 EP
#종결어미 EF
S = ["SF", "SP", "SS", "SE", "SO", "SW"]
#용언
V = ["VV", "VA", "VX"]
#접미사
X = ["XSN", "XSV", "XSA"]
N = ["NNG", "NNP"]

#XSV : 동사 파생형 접미사
#동사 파생 접미사 XSV
#EC 연결어미


def callKomoran(text):
    print("(코모란)형태소 분석중..")
    print(text)
    arr = komoran.pos(text)
    print(arr)
    print("형태소 분석 완료.")

    infinResult = ""
    infinResult = infinVerb(arr)

#    if ckUpper(arr) == 1:
 #       print("코모란 높임말")
  #  else:
   #     print("코모란 낯춤")

    # 동사가 높임말인지 검사

    return infinResult, ckUpper(arr)

#동사 원형 복원
def infinVerb(arr):

    upperflag = 1 #높임말 : 1, 아니면 -1
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


        if token2[1] in N:
            if not que:  # 만약 큐에 아무것도 없으면
                que.append(token2)
            else:
                if que[-1][1] in N:  # 만약 앞에 명사가 있으면(복합명사)
                    que.append(token2)
                else:  # 명사 앞에 그 이외의 값이면
                    que = []  # 배열 초기화
                    que.append(token2)

        elif token2[1] in V:

            if que:
                if que[-1][1] in N or que[-1][1] in "EF":  # 동사 앞의 값은 명사, EF만 올 수 있다.
                    que.append(token2)
                elif que[-1][1] == "EC":
                    que.append(token2)
                else:  # 만약 큐에 이상한 값 들어있으면
                    que = []
                    que.append(token2)
            else: #큐에 아무것도 없을 경우
                que.append(token2)

        elif token2[1] in X:
            if que:
                if que[-1][1] in N:
                    que.append(token2)
                else:
                    #print("큐초기화2")
                    que = []
            else:
                que.append(token2)
        elif token2[1] == "EC": #발벗고 나서다
            if que:
                if que[-1][1] in V:
                    que.append(token2)
                else:
                    #print("큐초기화3")
                    que = []
        #print(que)
    result = ""

    if que:
        for k in que:
            result = result +k[0]
        result = result + '다'
    return result

def ckUpper(tokens):
    for i in range(len(tokens)):
        if tokens[i][1] == "EP" and tokens[i][0] =='시' and tokens[i-1][1] in V:
            return 1 #높임말
        elif tokens[i][1] == "EP" and tokens[i][0] == '시' and tokens[i - 1][1] == 'XSV':
            return 1 #높임말
        elif tokens[i][1] == "EP" and tokens[i][0] == '으시' and tokens[i - 1][1] == 'XSV':
            return 1 #높임말
        elif tokens[i][1] == "EP" and tokens[i][0] =='으시'and tokens[i-1][1] in V:
            return 1 #높임말
    return -1 #높임말 아님
