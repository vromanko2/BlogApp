from rest_framework import serializers
from .models import Post, Blog, NewsFeed, UserSubscribers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


class PostSerializer(serializers.ModelSerializer):
    author = get_user_model()

    class Meta:
        model = Post
        fields = ('title', 'text', 'author', 'created_at')


class BlogSerializer(serializers.ModelSerializer):
    user = get_user_model()
    post = PostSerializer(required=False)

    class Meta:
        model = Blog
        fields = ('post', 'user')


class NewsFeedSerializer(serializers.ModelSerializer):
    user = get_user_model()

    class Meta:
        model = NewsFeed
        fields = ('user')


class UserSubscribersSerializer(serializers.ModelSerializer):
    user = get_user_model()
    subscribers = get_user_model()

    class Meta:
        model = UserSubscribers
        fields = ('user', 'subscribers')


class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'id')