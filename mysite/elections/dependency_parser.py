# -*- coding: utf-8 -*-

# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

# Instantiates a client
client = language.LanguageServiceClient()
# Detects the sentiment of the text

def findNSUBJ(text):
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)
    tokens = client.analyze_syntax(document).tokens
    nsubj = ""
    root = ""
    for token in tokens:
        # root만 추출
        if token.dependency_edge.label == enums.DependencyEdge.Label.NSUBJ:
            # rootDP = token  #주어 정보 클래스
            # subjNo = rootDP.dependency_edge.head_token_index    #주어의 위치
            nsubj = token.text.content
        elif token.dependency_edge.label == enums.DependencyEdge.Label.ROOT:
            root = token.text.content

    return tokens, nsubj, root
