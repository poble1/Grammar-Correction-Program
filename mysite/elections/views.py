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



#1. 처음 html에서 빈 입력공간 보여줌
#2. 입력 값 처리
# 구분? 빈공간 form get으로 /처리 post
def newpost(request):
    if request.method == "POST":
        form = PostForm(request.POST)

        qu = (request.POST.get('text'))
        qu = qu.strip("\n")

        print('start initializing : ', qu)
        kkma = Kkma()
        kkma.nouns('initializing')

        #형태소 분석 시작
        answer = ""
        answer = start(qu)

        if form.is_valid():
            return render(request, 'elections/output.html', {'string': answer})

    else:
        form = PostForm()
        return render(request, 'elections/index.html', {'form': form})

def start(qu):
    init = []

    #형태소 분석기 실행
    KkoArr, infinResult, cls1 = koko.callKokoma(qu)
    komoranResult = komo.callKomoran(qu)

    if infinResult == "-1": #만약 높임 표현이 아니면
        print("높임표현 의심")
        infinResult = komoranResult  #코모란 넣음

    # 만약 원형에 '시'가 있으면
    if ckInfin(infinResult) == 1:
        print("시 탐지")
        #코모란 실행
        infinResult = komoranResult

        # 만약 격틀사전에 없다면
    ckhuman = []
    if mg.ckVerbDic(infinResult) == -1:
        infinResult = komoranResult
    else:
        ckhuman = mg.ckVerbDic(infinResult)

    print("원형 : " + infinResult)
    print("동사-주어 관계:", ckhuman)

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
    verb=""
    #옳은 문장인지 체크
    corTag=cor.ckSent(isrightVerb, ishumanNoun)
    if corTag == -1: #옳지 않으면
        verb = cor.cgVerb(KkoArr)
        answer = cor.cgSent(qu, root, cls1)
    else:
        answer = "올바른 표현입니다."

    return answer

#'시' 유무 판단
def ckInfin(infinResult):
    tag = 0
    for k in infinResult:
        if k == "시":
            tag = 1
            print("'시'탐지")
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