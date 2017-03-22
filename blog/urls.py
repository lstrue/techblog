from django.conf.urls import url, include
from django.views.generic import ListView, DetailView
from blog.models import Post

from blog.views import post_create, post_delete, post_detail, post_list, post_update

urlpatterns = [
    url(r'^list/$', post_list, name='list'),
    url(r'^create/$', post_create),
    #url(r'^(?P<id>\d+)/$', post_detail),
    url(r'^(?P<slug>[\w-]+)/$', post_detail, name='detail'),
    url(r'^(?P<slug>[\w-]+)/update/$', post_update, name="update"),
    url(r'^(?P<slug>[\w-]+)/delete/$', post_delete),
    
    
    
#     url(r'^$', ListView.as_view(queryset = Post.objects.all().order_by("-timestamp")[:25],
#                                 template_name="blog/blog.html")),
#                
#     url(r'^(?P<pk>\d+)$', DetailView.as_view(model = Post,
#                                              template_name="blog/post.html")),
]