from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404

from django.contrib import messages

from .models import Post
from .blogforms import PostForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from urllib import quote_plus

from django.utils import timezone

from django.db.models import Q

def post_home(request):    
    return HttpResponse("<h1>Hello</h1>")

def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    if not request.user.is_authenticated():
        raise Http404
    
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit = False)
#         instance.user = request.user
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


#def post_detail(request, id=None):
def post_detail(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    if instance.draft:#or instance.publish > timezone.now().date(): 
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
        
#     share_string = quote_plus(instance.content)
    share_string = quote_plus(str(instance.content.encode("utf-8"))) #http://outofmemory.cn/code-snippet/835/python-urllib-quote-huozhe-quote-plus-paochu-keyError-jiejuefangan
    context = {
        "name": "List",
        "obj": instance,
        "share_string": share_string,
    }
    print "======" + share_string
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
    
#     queryset_list = Post.objects.all().order_by("-timestamp")
#     queryset_list = Post.objects.filter(draft=False).filter(publish_lte=timezone.now())
#     queryset_list = Post.objects.filter(draft=False)
    
#     queryset_list = Post.objects.all()
    queryset_list = Post.objects.active().order_by("-timestamp")

    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all().order_by("-timestamp")
    
    query = request.GET.get("q")
    if query:
#         queryset_list = queryset_list.filter(title__icontains=query)
        
        queryset_list = queryset_list.filter(
        Q(title__icontains=query) |
        Q(content__icontains=query) |
        Q(user__first_name__icontains=query) |
        Q(user__last_name__icontains=query)
        ).distinct().order_by("-timestamp")
    
    paginator = Paginator(queryset_list, 5)
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
    
    context = {
        "object_list": queryset,
        "name": "List",
        "page_request_var": page_request_var
    }    
    return render(request, "post_list.html", context)

def post_update(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        #message success
        messages.success(request, "successfully saved")
#         messages.success(request, "<a href='#'>Item</a> Saved", extra_tags="html_safe")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "name": instance.title,
        "obj": instance,
        "form": form,
    }
    return render(request, "post_form.html", context)

def post_delete(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    messages.success(request, "successfully deleted")
    return redirect("blog:list")