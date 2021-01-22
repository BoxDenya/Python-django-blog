from django.db import models
from django.urls import reverse


class News(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименование')
    content = models.TextField(blank=True, verbose_name='Контент')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Фото', blank=True)
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')
    views = models.IntegerField(default=0)  # поле количество просмотров по умолчанию просмотров 0

    def get_absolute_url(self):
        return reverse('view_news', kwargs={"pk": self.pk})  # редирект на добавленную новость

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'  # единственное число
        verbose_name_plural = 'Новости'  # множественное число
        ordering = ['-created_at']  # порядок сортировки новостей


class Category(models.Model):
    title = models.CharField(max_length=150, db_index=True, verbose_name='Наименование категории')

    # Джанго сам выстраивает адрес url при использовании данного метода и связывает в данном случае категории с админкой
    def get_absolute_url(self):
        return reverse('category', kwargs={"category_id": self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'  # единственное число
        verbose_name_plural = 'Категории'  # множественное число
        ordering = ['title']  # сортировка новостей