
from django.db import models
from datetime import date
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.


class BlogAuthor(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    bio = models.TextField(
        max_length=400, help_text="Enter your Bio details here.")

    class Meta:
        ordering = ['user', 'bio']

    def get_absolute_url(self):
        return reverse('blogs-by-author', args=[str(self.id)])

    def __str__(self):
        return self.user.username


class Blog(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    author = models.ForeignKey(
        BlogAuthor, on_delete=models.SET_NULL, null=True)
    description = models.TextField(
        max_length=2000, help_text="Enter your blog text here.")
    post_date = models.DateField(default=date.today)

    class Meta:
        ordering = ['-post_date']

    def get_absolute_url(self):
        return reverse('blog-detail', args=[str(self.id)])

    def __str__(self):
        return self.name


class BlogComment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True)
    description = models.TextField(
        max_length=1000, help_text="Enter your comment about blog here.")
    post_date = models.DateField(auto_now_add=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

    class Meta:
        ordering = ['post_date']

    def __str__(self):
        len_title = 75
        if len(self.description) > len_title:
            title = self.description[:len_title]+'...'
        else:
            title = self.description
        return title
