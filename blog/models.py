from __future__ import unicode_literals

# Create your models here.

from django.db import models
from django.core.urlresolvers import reverse

def upload_location(obj, filename):
#     filebase, extension = filename.split(".")
#     return "%s/%s.%s" %(instance.id, instance.id, extension)
    return "%s/%s" %(obj.id, filename) # later on you can upload images based on user id

class Post(models.Model):
    title = models.CharField(max_length = 140)
    
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
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
#         return "/blog/%s/" %(self.id)
#        return reverse("detail", kwargs={"id": self.id})
        return reverse("blog:detail", kwargs={"id": self.id})
    
    #class Meta:
    #    ordering = ["-timestamp", "-updated"]