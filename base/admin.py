from django.contrib import admin

from .models import Blog, BlogAuthor, BlogComment

# Register your models here.
admin.site.register(BlogAuthor)
admin.site.register(BlogComment)


class BlogCommentInline(admin.TabularInline):
    model = BlogComment
    max_num = 0


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'post_date')
    inlines = [BlogCommentInline]
