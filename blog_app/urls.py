from django.urls import path
from .views import ListBlogPostsView, BlogPostsView, ListUsers, UserSubscribeView, UserUnsubscribeView, UserNewsFeedView


urlpatterns = [
    path('blogs/', ListBlogPostsView.as_view(), name="blogs-all"),
    path('blogs/<int:pk>/posts/', BlogPostsView.as_view(), name="blog_posts-all"),
    path('users/', ListUsers.as_view(), name="users-all"),
    path('user/<int:pk>/subscribe/', UserSubscribeView.as_view(), name="subscribe"),
    path('user/<int:pk>/unsubscribe/', UserUnsubscribeView.as_view(), name="subscribe"),
    path('user/<int:pk>/news_feed/', UserNewsFeedView.as_view(), name="news_feed"),
]