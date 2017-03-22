from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from .models import Post

def post_home(request):    
    return HttpResponse("<h1>Hello</h1>")

def post_create(request):
    queryset = Post.objects.all()
    context = {
        "object_list": queryset,
        "name": "List",
    }    
    return render(request, "index.html", context)

def post_detail(request):
    if request.user.is_authenticated():
        context = {
            "name": "David"
        }
    else:
        context = {
            "name": "Not auth"
        }
    return render(request, "index.html", context)

def post_list(request):
    return render(request, "index.html", {})
#     return HttpResponse("<h1>list</h1>")

def post_update(request):    
    return HttpResponse("<h1>update</h1>")

def post_delete(request):    
    return HttpResponse("<h1>delete</h1>")