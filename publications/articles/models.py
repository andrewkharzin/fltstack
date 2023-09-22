from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from unidecode import unidecode
from mptt.models import MPTTModel, TreeForeignKey


def get_image_upload_path(instance, filename):
    category_name = instance.category.name if instance.category else 'uncategorized'
    year = instance.date_created.strftime('%Y')
    month = instance.date_created.strftime('%m')
    return os.path.join('featured_images', category_name, year, month, filename)


class Category(MPTTModel):
    name = models.CharField(max_length=100)
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = TreeForeignKey(Category, on_delete=models.CASCADE)
    featured_image = models.ImageField(
        upload_to=get_image_upload_path, null=True, blank=True)
    slug = models.SlugField(max_length=200, unique=True)  # New slug field

    def save(self, *args, **kwargs):
        # Generate slug only if it's not already set
        if not self.slug:
            # Transliterate the title and generate the slug
            transliterated_title = unidecode(self.title)
            self.slug = slugify(transliterated_title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(MPTTModel):
    article = models.ForeignKey(
        Article, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='replies')

    class MPTTMeta:
        order_insertion_by = ['date_created']

    def __str__(self):
        return f'Comment by {self.author.username} on {self.article.title}'
