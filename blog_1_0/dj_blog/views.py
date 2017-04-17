#coding:gbk

from django.http import HttpResponse
from django.shortcuts import render_to_response


def test(request):
    return  render_to_response('index.html')

def article(request):
    return  render_to_response('blog.html')