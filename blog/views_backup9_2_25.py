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

from django.contrib.contenttypes.models import ContentType
from comments.models import Comment

from comments.commentforms import CommentForm

from .utils import get_read_time

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
    
    #the meaning of the bellow: Post.objects.get(id=instance.id)
    #content_type = ContentType.objects.get_for_model(Post)
    #obj_id = instance.id
    #comments = Comment.objects.filter(content_type=content_type, object_id=obj_id)
    
    #after using model manager and put logic to model, the view is very clean
    comments = instance.comments()
    
    print(get_read_time(instance.content))
    print(get_read_time(instance.get_markdown()))
    
    
    initial_data = {
        "content_type": instance.get_content_type(),
        "object_id": instance.id
    }
    #user comment form
    form = CommentForm(request.POST or None, initial = initial_data)
    if form.is_valid():
        c_type = form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type) #content type
        obj_id = form.cleaned_data.get("object_id") #obj id
        content_data = form.cleaned_data.get("content") #content
        
        
        parent_obj = None
        try:
            parent_id = int(request.POST.get("parent_id"))#key worrd for search "parent_id"
        except:
            parent_id = None
        
        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id) # based on comment id get comment reply children
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()
        
        #create comment and comment reply
        new_comment, created = Comment.objects.get_or_create(
            user = request.user, content_type=content_type,
            object_id = obj_id, content = content_data,
            parent_for_reply = parent_obj
        )
    
    
    context = {
        "name": "List",
        "obj": instance,
        "share_string": share_string,
        "comments": comments,
        "comment_form": form,
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