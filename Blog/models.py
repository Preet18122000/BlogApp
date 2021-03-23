from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')

class DraftManager(models.Manager):
    def get_queryset(self):
        return super(DraftManager, self).get_queryset().filter(status='draft')


class Post(models.Model):
    # Request status is defined using status_choices in which draft means just like email
    # and published is like email send
    STATUS_CHOICES = (
        ('draft','Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=500)
    slug = models.CharField(max_length=500, unique_for_date='publish')
    author	=	models.ForeignKey(User,on_delete=models.CASCADE,related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    objects = models.Manager()  # The default Mananger
    published = PublishedManager() # Our custom manager
    draft = DraftManager() 

    def get_absolute_url(self):
        return reverse("Blog:post_detail", args=[self.publish.year, self.publish.month, self.publish.day, self.slug])
        
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now = True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f"Comment by {self.name} on {self.post}"