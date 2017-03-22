from django.shortcuts import render, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.contrib import messages

from .commentforms import CommentForm
from .models import Comment


# Create your views here.


def comment_thread(request, id):
    instance = get_object_or_404(Comment, id=id)
    
    content_object = instance.content_object
    content_id = instance.content_object.id
    
    initial_data = {
        #"content_type": instance.get_content_type(),
        #"object_id": instance.id
        "content_type": instance.content_type,
        "object_id": instance.object_id
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
        
        #this line is added
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())
    
    context = {
        "comment": instance,
        "comment_form": form,
    }
    return render(request, "comment_thread.html", context)    

def comment_delete(request, id):
    #instance = get_object_or_404(Comment, id=id)
    #instance = Comment.objects.get(id=id)
    try:
        instance = Comment.objects.get(id=id)
    except:
        raise Http404
    
    if instance.user != request.user:
        response = HttpResponse("Permission denied")
        response.status_code = 403
        return response
   
    
    if request.method == "POST":
        #parent_obj_url = instance.content_object.get_absolute_url()
        instance.delete()
        messages.success(request, "This has been deleted.")
        return HttpResponseRedirect(instance.content_object.get_absolute_url())
    
    context = {
        "comment": instance
    }
    return render(request, "comment_delete.html", context)    
