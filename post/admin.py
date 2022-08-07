from xml.etree.ElementTree import Comment
from django.contrib import admin

from post.models import Post, Comment, Reply

# Register your models here.

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Reply)
