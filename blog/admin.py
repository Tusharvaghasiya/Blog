from django.contrib import admin
from blog.models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'created', 'updated', 'status']
    list_filter = ('status', 'author', 'created')
    search_fields=('author__username', )
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']
    prepopulated_fields = {'slug': ('title', )}
    

admin.site.register(Post, PostAdmin)