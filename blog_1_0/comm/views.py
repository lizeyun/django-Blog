from django.shortcuts import render_to_response

from django.http import HttpResponse
from models import Post, Replay
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
import datetime
import json

def index(request):
    posts = Post.objects.all()
    return render_to_response('index.html', {'posts' :posts})

@csrf_exempt
def comm(request, post_id):
    print 'use comm'

    if request.is_ajax():
        print 'cur is ajax req'
        replay_content = request.POST.get('replay_content', '')
        print 'post is %s'%request.POST.get('replay_user', '')
        if replay_content:
            item = Post.objects.get(id= post_id)
            Replay.objects.create(replay_content= replay_content, post= item)

        return HttpResponse(json.dumps({"content" :replay_content}))

    else:
        post_id = post_id
        content = Post.objects.get(id= post_id)
        replays = Post.objects.get(id= post_id).replay_set.all()
        return render_to_response('form.html', {'content': content, 'replays': replays},
                      content_type= RequestContext(request))
