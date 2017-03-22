from django import forms

from pagedown.widgets import PagedownWidget, AdminPagedownWidget

from .models import Post

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget())
    publish = forms.DateField(widget=forms.SelectDateWidget)
    
    #for admin
    content = forms.CharField(widget=AdminPagedownWidget())#show_preview=False
    
    class Meta:
        model = Post
        fields = ["title", "image", "content", "draft", "publish", ]