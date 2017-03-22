from django.contrib import admin

# Register your models here.
from blog.models import Post

class PostModelAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "updated", "timestamp"]
#     list_display_links = ["title", "updated"]
    search_fields = ["title"]
#     list_editable = ["title"]
    list_filter = ["updated"]
    class Meta:
        model = Post

admin.site.register(Post, PostModelAdmin)

