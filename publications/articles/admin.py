from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import Article, Category

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date_created', 'category')
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, DraggableMPTTAdmin)