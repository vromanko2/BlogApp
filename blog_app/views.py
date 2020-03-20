from django.shortcuts import render
from .models import Blog, Post, UserSubscribers, NewsFeed
from rest_framework import generics
from .serializers import PostSerializer, BlogSerializer, NewsFeedSerializer, UserSubscribersSerializer, CurrentUserSerializer
from rest_framework.response import Response
from rest_framework.views import status
from django.contrib.auth.models import User
from django.core.mail import send_mail

# Create your views here.


class ListBlogPostsView(generics.ListAPIView):
    """
            GET blogs/posts
    """

    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


class BlogPostsView(generics.RetrieveUpdateDestroyAPIView):
    """
            GET blogs/:pk/posts
    """

    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    def get(self, request, *args, **kwargs):
        try:
            set = self.queryset.filter(pk=kwargs['pk'])

            serializer = BlogSerializer(set, many=True)
            return Response(serializer.data)
        except Blog.DoesNotExist:
            return Response(
                data={
                    "message": "Book with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )


# class ListUsers(APIView):
#     def get(self, request, format=None):
#         """
#         Return a list of all users.
#         """
#         usernames = [user.username for user in User.objects.all()]
#         return Response(usernames)


class ListUsers(generics.ListAPIView):
    """
            GET users/
    """
    queryset = User.objects.all()
    serializer_class = CurrentUserSerializer


class UserSubscribeView(generics.RetrieveUpdateDestroyAPIView):
    """
                GET user/:pk/subscribe/
    """

    queryset = User.objects.all()
    serializer_class = CurrentUserSerializer

    def put(self, request, *args, **kwargs):
        try:
            current_user = self.queryset.get(pk=kwargs['pk'])
            # user_to_add = self.queryset.get(pk=kwargs['pk_2'])
            user_to_add = self.queryset.get(pk=request.data['id'], username=request.data["username"])
            if not user_to_add:
                return Response(
                    data={
                        "message": "User {} does not exist".format(request.data)
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            current_user_subscribers = UserSubscribers.objects.get(user=current_user)
            current_user_subscribers.subscribers.add(user_to_add)
            current_user_subscribers.save()

            add_posts_to_news_feed(current_user, user_to_add)

            return Response(status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(
                data={
                    "message": "User with id: {} does not exist".format(kwargs['pk'])
                },
                status=status.HTTP_404_NOT_FOUND
            )


def add_posts_to_news_feed(current_user, user_to_add):
    current_user_news_feed = NewsFeed.objects.get(user=current_user)
    print(current_user_news_feed)
    blog = Blog.objects.get(user=user_to_add)
    new_user_posts = Post.objects.filter(blog=blog)
    # current_user_news_feed.posts = new_user_posts
    # current_user_news_feed.save()
    # print(str(current_user_news_feed.post))
    for post in new_user_posts:
        post.news_feed = current_user_news_feed
        print(post.news_feed)
        post.save()


class UserUnsubscribeView(generics.RetrieveUpdateDestroyAPIView):
    """
                GET user/:pk/subscribe/
    """

    queryset = User.objects.all()
    serializer_class = CurrentUserSerializer

    def put(self, request, *args, **kwargs):
        try:
            current_user = self.queryset.get(pk=kwargs['pk'])
            # user_to_add = self.queryset.get(pk=kwargs['pk_2'])
            user_to_unsubscribe = self.queryset.get(pk=request.data['id'], username=request.data["username"])
            if not user_to_unsubscribe:
                return Response(
                    data={
                        "message": "User {} does not exist".format(request.data)
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            current_user_subscribers = UserSubscribers.objects.get(user=current_user)
            current_user_subscribers.subscribers.remove(user_to_unsubscribe)
            current_user_subscribers.save()

            delete_posts_from_news_feed(current_user, user_to_unsubscribe)

            return Response(status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(
                data={
                    "message": "User with id: {} does not exist".format(kwargs['pk'])
                },
                status=status.HTTP_404_NOT_FOUND
            )


def delete_posts_from_news_feed(current_user, user_to_unsubscribe):
    current_user_news_feed = NewsFeed.objects.get(user=current_user)
    print(current_user_news_feed)
    blog = Blog.objects.get(user=user_to_unsubscribe)
    user_to_delete_posts = Post.objects.filter(blog=blog)
    for post in user_to_delete_posts:
        post.news_feed = None
        print(post.news_feed)
        post.save()


class UserNewsFeedView(generics.RetrieveUpdateDestroyAPIView):
    """
                GET user/:pk/news_feed/
    """

    queryset = User.objects.all()
    serializer_class = CurrentUserSerializer

    def get(self, request, *args, **kwargs):
        try:
            current_user = self.queryset.get(pk=kwargs['pk'])

            current_user_news_feed = NewsFeed.objects.get(user=current_user)
            posts = Post.objects.filter(news_feed=current_user_news_feed).order_by('-created_at')
            print(str(posts))
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(
                data={
                    "message": "User with id: {} does not exist".format(kwargs['pk'])
                },
                status=status.HTTP_404_NOT_FOUND
            )
