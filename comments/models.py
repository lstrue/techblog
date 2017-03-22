from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.conf import settings
#from blog.models import Post

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from Carbon.Aliases import false

from django.core.urlresolvers import reverse

#get comments based on instance and id
class CommentManager(models.Manager): 
    def get_all(self):
        qs = super(CommentManager, self).filter(parent_for_reply=None)
        return qs
    
    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        #comments = Comment.objects.filter(content_type=content_type, object_id=obj_id)
        
        #qs = super(CommentManager, self).filter(content_type=content_type, object_id=obj_id)
        qs = super(CommentManager, self).filter(content_type=content_type, object_id=obj_id).filter(parent_for_reply=None)
        
        return qs


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    
#     post = models.ForeignKey(Post)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    
    
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    parent_for_reply = models.ForeignKey("self", null=True, blank=True)
    
    
    objects = CommentManager()
    
    
    def __unicode__(self):
        return str(self.user.username)
    
    def __str__(self):
        return str(self.user.username)
    
    
    #reply
    def get_comment_children(self):
        return Comment.objects.filter(parent_for_reply=self)
    
    """
    def is_parent(self):
        if self.parent_for_reply is not None:
            return False
        return True
    """
    
    def get_absolute_url(self):
        return reverse("comments:thread", kwargs={"id": self.id})
    
    def get_delete_url(self):
        return reverse("comments:delete", kwargs={"id": self.id})