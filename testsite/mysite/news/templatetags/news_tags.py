from django import template
from django.db.models import Count, F
from django.core.cache import cache

from news.models import Category

register = template.Library()  # Регистрация templatetags


# Создание собственного тега simple_tag для вывода категорий(чтобы в контроллере в каждом методе не создавать переменную категории)
@register.simple_tag(name='get_list_categories')
def get_categories():
    return Category.objects.all()


# Рендеринг данных в шаблон (inclusion_tag - рендерит данные в шаблон list_categories)
@register.inclusion_tag('news/list_categories.html')
def show_categories(arg1='Hello', arg2='world'):
    # categories = cache.get('categories')
    # if not categories:
    #
    #
    # # categories = Category.objects.all()
    # #     categories = Category.objects.annotate(cnt=Count('news')).filter(cnt__gt=0)  # выводим только опубликованные категории, а пустые не выводим
    #     categories = Category.objects.annotate(cnt=Count('news', filter=F('news__is_published'))).filter(cnt__gt=0)  # выводим только обубликованные категории, а пустые не выводим( в count считаем только опубликованные новости)
    #     cache.set('categories', categories, 30)
    
    categories = Category.objects.annotate(cnt=Count('news', filter=F('news__is_published'))).filter(
        cnt__gt=0)  # выводим только обубликованные категории, а пустые не выводим( в count считаем только опубликованные новости)
    return {"categories": categories, "arg1": arg1, "arg2": arg2}