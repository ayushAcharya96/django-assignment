from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse, reverse_lazy
from django.utils.text import slugify

USER = get_user_model()

class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    content = models.TextField()
    slug = models.SlugField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(USER, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        kwargs = {
            'slug': self.slug
        }
        return reverse_lazy('blogs:post-detail', kwargs=kwargs)

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args,**kwargs)