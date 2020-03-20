from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from django.contrib import admin

# Create your models here.


class NewsFeed(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # posts = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.username + "_newsfeed"


class Blog(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # post = models.ForeignKey(Post, blank=True, on_delete=models.CASCADE, null=True)

    # def save(self, *args, **kwargs):
    #     print(str(self.post.author))
    #     found = False
    #     for i in self.post.all():
    #         if i.author != self.user:
    #             found = True
    #     if found:
    #         raise Exception("Bad author")
    #     else:
    #         super(Blog, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username + "_blog"


class Post(models.Model):
    title = models.CharField(max_length=20, blank=False, null=False)
    text = models.TextField(max_length=120, blank=False, null=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    news_feed = models.ForeignKey(NewsFeed, related_name='news_feeds', on_delete=models.CASCADE, null=True, blank=True)
    # news_feed = models.ManyToManyField(NewsFeed, blank=True)
    blog = models.ForeignKey(Blog, related_name='blog', on_delete=models.CASCADE, null=False, blank=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.author:
            self.author = self.blog.user
            super(Post, self).save(*args, **kwargs)

        all_this_author_posts = Post.objects.filter(author=self.author)
        print(all_this_author_posts)
        people = []
        for post in all_this_author_posts:
            news_feed = post.news_feed
            if news_feed:
                people.append(news_feed.user.id)
        people = list(set(people))
        people_qs = User.objects.filter(id__in=people)
        print(people_qs)
        for user in people_qs:
            if user.email:
                send_mail(
                    'New post',
                    'User created a new post',
                    self.author.email,
                    [user.email],
                    fail_silently=False
                )
            print(user.email)

        # user_news_feed = NewsFeed.objects.get(user=self.author)
        # print(self.author)
        # posts = Post.objects.filter(news_feed=user_news_feed)
        # print(posts)
        # people = []
        # for post in posts:
        #     people.append(post.author)
        # print(people)

        # send_mail(
        #     'New post',
        #     'User created a new post',
        #     'from@example.com',
        #     ['to@example.com'],
        #     fail_silently=False
        # )

    def __str__(self):
        return self.title


class UserSubscribers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscribers = models.ManyToManyField(User, blank=True, related_name='subscribers')

    def __str__(self):
        return self.user.username + "_subscribtions"


@receiver(post_save, sender=User)
def create_user_subscribers(sender, instance, created, **kwargs):
    if created:
        UserSubscribers.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_subscribers(sender, instance, **kwargs):
    instance.usersubscribers.save()


@receiver(post_save, sender=User)
def create_user_newsfeed(sender, instance, created, **kwargs):
    if created:
        NewsFeed.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_newsfeed(sender, instance, **kwargs):
    instance.newsfeed.save()


@receiver(post_save, sender=User)
def create_user_blog(sender, instance, created, **kwargs):
    if created:
        Blog.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_blog(sender, instance, **kwargs):
    instance.blog.save()

