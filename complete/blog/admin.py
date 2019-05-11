from django.contrib import admin
from blog.models import post, comment

admin.site.register(post)
admin.site.register(comment)