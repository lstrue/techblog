"""Spruceandfresh9 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

#from blog.views import post_home
# from blog import views
# from blog.views import a, b, c

from django.conf import settings
from django.conf.urls.static import static

from accounts.views import login_view, logout_view, register_view

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
#     url(r'^blog/$', post_home),
    #url(r'^blog/', include('blog.urls')),
    url(r'^blog/', include('blog.urls', namespace="blog")),
    url(r'^ecom/', include('ecom.urls')),
    url(r'^comments/', include('comments.urls', namespace="comments")),
    url(r'^login/', login_view, name='login'),
    url(r'^logout/', logout_view, name='logout'),
    url(r'^register/', register_view, name='register'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 
    #static(/static/, document_root=Spruceandfresh9/static_cdn)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    #static(/media/, document_root=Spruceandfresh9/media_cdn)
    