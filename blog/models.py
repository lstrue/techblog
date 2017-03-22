from __future__ import unicode_literals

# Create your models here.

from django.db import models
from django.core.urlresolvers import reverse

class Post(models.Model):
    title = models.CharField(max_length = 140)
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