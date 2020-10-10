from django.conf import settings
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
        ordering = ['title']


class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='items/', blank=True)

    class Meta:
        verbose_name = "Фото товара"
        verbose_name_plural = "Фото товаров"

    def __str__(self):
        return '{} # {}'.format(self.item.title, self.id)


class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.item.title} - {self.quantity}'

    def total_amount(self):
        print(self.quantity * self.item.discount_price if self.item.discount_price else self.quantity * self.item.price)
        return self.quantity * self.item.discount_price if self.item.discount_price else self.quantity * self.item.price


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def total_order_amount(self):
        result = 0
        for item in self.items.all():
            result += item.total_amount()
            print(result)
        print(result)
        return result







