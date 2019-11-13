# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponseRedirect
from konlpy.tag import Kkma
from konlpy.utils import pprint
import sys

from . import dependency_parser as dp
from . import KokomaQuever7 as koko
from . import Komoran3que2 as komo
from . import searchMongo as mg
from . import corSent as cor
from .models import Content
from .form import PostForm

# Create your views here.
def index(request):
    if request.method == "GET":
        return HttpResponseRedirect('input')

def solve(request,  categ_name=None, subcateg_name=None):
    verb = categ_name
    subj = subcateg_name
    return render(request, 'elections/solve.html', {'verb': verb, 'subj': subj})

def info(request):
    return render(request, 'elections/info.html')

def changeH(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        qu = (request.POST.get('text'))
        ##qu에 문장들 들어온다
        texts = []

        sentList = []
        result = ""

        kkma = Kkma()
        texts = kkma.sentences(qu)
        for text in texts:
            text = text.strip("\n")
            print('start initializing : ', text)
            kkma = Kkma()
            kkma.nouns('initializing')

            #형태소 분석 시작
            answer, LVerb = start2(text)

            temp = []
            temp.append(answer)
            temp.append(LVerb)
            sentList.append(temp)

            ## 리스트 [['주문하신 커피가 ', '나오셨습니다.', '나왔습니다']]
            #print(sentList)


        if form.is_valid():
            return render(request, 'elections/changeHoutput.html', {'sentList': sentList})

    else:
        form = PostForm()
        return render(request, 'elections/changeH.html', {'form': form})

#1. 처음 html에서 빈 입력공간 보여줌
#2. 입력 값 처리
# 구분? 빈공간 form get 으로 /처리 post

def newpost(request):
    if request.method == "POST":
        form = PostForm(request.POST)

        qu = (request.POST.get('text'))
        ##qu에 문장들 들어온다
        texts = []

        sentList = []
        result = ""

        kkma = Kkma()
        texts = kkma.sentences(qu)
        for text in texts:
            text = text.strip("\n")
            print('start initializing : ', text)
            kkma = Kkma()
            kkma.nouns('initializing')

            #형태소 분석 시작
            answer, rowVerb, rightVerb, subj = start(text)

            temp = []
            temp.append(answer)
            temp.append(rowVerb)
            temp.append(rightVerb)
            temp.append(subj)
            sentList.append(temp)

            ## 리스트 [['주문하신 커피가 ', '나오셨습니다.', '나왔습니다']]
            #print(sentList)


        if form.is_valid():
            return render(request, 'elections/output.html', {'sentList': sentList})

    else:
        form = PostForm()
        return render(request, 'elections/index.html', {'form': form})

def start(qu):
    init = []

    #형태소 분석기 실행
    KkoArr, infinResult, cls1, upperflag1 = koko.callKokoma(qu)
    KomoArr, komoranResult, upperflag2 = komo.callKomoran(qu)
    upperflag = upperflag1
    iscomoran = False


    if upperflag1 == "-1": #만약 높임 표현이 아니면
        print("높임표현 의심")
        infinResult = komoranResult  #코모란 넣음
        upperflag = upperflag2

    # 만약 원형에 '시'가 있으면
    if ckInfin(infinResult) == 1:
        print("시 탐지")
        #코모란 실행
        infinResult = komoranResult
        upperflag = upperflag2

    # 만약 격틀사전에 없다면
    ckhuman = []
    if mg.ckVerbDic(infinResult) == -1:
        infinResult = komoranResult
        upperflag = upperflag2
    else:
        ckhuman = mg.ckVerbDic(infinResult)

    print("원형 : " + infinResult)
    print("동사-주어 관계:", ckhuman)

    if upperflag == -1:
        return qu, "-1", ""
# 그 동사가 인간에 쓰일 수 있는지 가능:1, 블가:-1
    isrightVerb = ckVerbHuman(ckhuman)
    dpTokens, subj, root = dp.findNSUBJ(qu)
    print('주어 : ', subj)

    # 주어가 없는 문장이면
    if subj == None:
        subj = '온'

# 사람인지 판단 1:사람 0:인간이거나 아님 외:인간 아님
    ishumanNoun = mg.ckNounbDic(subj)

    if isrightVerb == -1:
        print("높임말 사용 불가 동사")
    else:
        print("높임말 사용 가능 동사")

    print("주어 범주: ", subj)

    if ishumanNoun == 1:
        print("인간임")
    elif ishumanNoun == 0:
        print("인간 or 인간 아님")
    else:
        print("인간 아님")

    answer = ""

    temp = qu.split(" ")

    verb = ""
    rowVerb = temp[-1]

    if(infinResult == -1):
        answer = qu
        rowVerb = "-1"
        return answer, rowVerb, verb

    #옳은 문장인지 체크
    corTag = cor.ckSent(isrightVerb, ishumanNoun, upperflag)

    if corTag == -1: #옳지 않으면
        if (iscomoran):
            verb = cor.cgVerb(KomoArr)
            answer = cor.cgSent(qu, rowVerb)
        else:
            verb = cor.cgVerb(KkoArr)
            answer = cor.cgSent(qu, rowVerb)
    else:
        answer = qu
        rowVerb = "-1"

    return answer, rowVerb, verb, subj

def start2(qu):
    init = []

    #형태소 분석기 실행
    KkoArr, infinResult, cls1, upperflag1 = koko.callKokoma(qu)
    KomoArr, komoranResult, upperflag2 = komo.callKomoran(qu)
    upperflag = upperflag1

    iscomoran = False

    if upperflag1 == "-1": #만약 높임 표현이 아니면
        print("높임표현 의심")
        infinResult = komoranResult  #코모란 넣음
        upperflag = upperflag2
        iscomoran = True

    # 만약 원형에 '시'가 있으면
    if ckInfin(infinResult) == 1:
        print("시 탐지")
        #코모란 실행
        infinResult = komoranResult
        upperflag = upperflag2
        iscomoran = True

    temp = qu.split(" ")

    verb = ""
    rowVerb = temp[-1]

    if(infinResult == -1):
        answer = qu
        return answer, verb

    # 낮추기
    if(iscomoran):
        verb = cor.cgVerb(KomoArr)
        answer = cor.cgSent(qu, rowVerb)
    else:
        verb = cor.cgVerb(KkoArr)
        answer = cor.cgSent(qu, rowVerb)

    return answer, verb + cls1



#'시' 유무 판단
def ckInfin(infinResult):
    tag = 0
    for k in infinResult:
        if k == "시":
            tag = 1
    return tag

def ckVerbHuman(arr):
    if '인간' in arr:
        return 1
    #elif '신체일부'
    return -1

def output(request):
    contents = Content.objects.all()
    context = {'contents': contents} #context에 모든 정보를 저장
    return render(request, 'elections/output.html', context)


