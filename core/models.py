from django.db import models
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Item(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='items/', default='default.jpg')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('item-detail', kwargs={'category_slug': self.category.slug, 'item_slug': self.slug})

    def get_discount_percent(self):
        return round(100 - (self.discount_price / self.price) * 100)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

