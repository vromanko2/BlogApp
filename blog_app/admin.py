from django.contrib import admin
from .models import Post, Blog, UserSubscribers, NewsFeed
# Register your models here.


class PostInline(admin.TabularInline):
    model = Post


class NewsFeedAdmin(admin.ModelAdmin):
    inlines = [
        PostInline,
    ]


class BlogAdmin(admin.ModelAdmin):
    inlines = [
        PostInline
    ]


admin.site.register(Post)
admin.site.register(Blog, BlogAdmin)
admin.site.register(UserSubscribers)
admin.site.register(NewsFeed, NewsFeedAdmin)