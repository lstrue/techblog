from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib import messages

from .models import Post
from .blogforms import PostForm

def post_home(request):    
    return HttpResponse("<h1>Hello</h1>")

def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit = False)
        instance.save()
        #message success
        messages.success(request, "successfully created")
        return HttpResponseRedirect(instance.get_absolute_url())
    #if form.errors:
    #else:
    #    messages.error(request, "failed")
    context = {
        "form": form,
    }
    return render(request, "post_form.html", context)
#     return HttpResponse("<h1>list</h1>")


def post_detail(request, id=None):
    instance = get_object_or_404(Post, id=id)
    context = {
        "name": "List",
        "obj": instance,
    }
    return render(request, "post_detail.html", context)    

# def post_detail(request):
#     if request.user.is_authenticated():
#         context = {
#             "name": "David"
#         }
#     else:
#         context = {
#             "name": "Not auth"
#         }
#     return render(request, "index.html", context)

def post_list(request):    
#     instance = Post.objects.get(id=6)
#     instance = get_object_or_404(Post, id=21)
#    instance = get_object_or_404(Post, title=21)
    
    #return render(request, "index.html")
    
    queryset = Post.objects.all()
    context = {
        "object_list": queryset,
        "name": "List",
    }    
    return render(request, "index.html", context)

def post_update(request, id=None):
    print "id: " + id
    
    instance = get_object_or_404(Post, id=id)
    
    print instance.title
        
    form = PostForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        #message success
        messages.success(request, "successfully saved")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "name": instance.title,
        "obj": instance,
        "form": form,
    }
    return render(request, "post_form.html", context)

def post_delete(request, id=None):
    instance = get_object_or_404(Post, id=id)
    instance.delete()
    messages.success(request, "successfully deleted")
    return redirect("blog:list")