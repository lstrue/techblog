from __future__ import unicode_literals

# Create your models here.

from django.db import models
from django.core.urlresolvers import reverse

from django.db.models.signals import pre_save
from django.utils.text import slugify

from django.conf import settings

from django.utils import timezone

class PostManager(models.Manager):
#     def all(self, *args, **kwargs):
    def active(self, *args, **kwargs):
        # Post.object.all() = super(PostManager, self).all()
#         return super(PostManager, self).filter(draft=False).filter(publish_lte=timezone.now())
        return super(PostManager, self).filter(draft=False)

def upload_location(obj, filename):
#     filebase, extension = filename.split(".")
#     return "%s/%s.%s" %(instance.id, instance.id, extension)
    return "%s/%s" %(obj.id, filename) # later on you can upload images based on user id

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default = 1)
    title = models.CharField(max_length = 140)
    slug = models.SlugField(unique=True)
    image = models.ImageField(
            upload_to=upload_location,
            null = True, #db
            blank = True, #form
            width_field="width_field",
            height_field="height_field"
            )
    width_field = models.IntegerField(default=0)
    height_field = models.IntegerField(default=0)
    
    content = models.TextField()
    
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False)
    
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = PostManager()

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
#         return "/blog/%s/" %(self.id)
#        return reverse("detail", kwargs={"id": self.id})

        #return reverse("blog:detail", kwargs={"id": self.id})
        return reverse("blog:detail", kwargs={"slug": self.slug})
    
    #class Meta:
    #    ordering = ["-timestamp", "-updated"]

#This function basically recursively combine the title string replacing space with -
def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug
    
def pre_save_post_receiver(sender, instance, *args, **kwargs): # here the second argument has to be named instance 
    if not instance.slug:
        instance.slug = create_slug(instance)
        
pre_save.connect(pre_save_post_receiver, sender=Post)
