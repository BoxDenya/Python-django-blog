from django.urls import path
from django.views.decorators.cache import cache_page

from .views import *

urlpatterns = [
    path('regisrer/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('contact/', contact, name='contact'),
    path('test/', test, name='test'),
    # path('', index, name='home'),  # маршрут метод для модели News
    # path('', cache_page(60)(HomeNews.as_view()), name='home'),  # кешируем главную страницу
    path('', HomeNews.as_view(), name='home'),  # маршрут для класса модели News
    # path('category/<int:category_id>/', get_category, name='category'),  # маршрут метод для модели Category
    path('category/<int:category_id>/', NewsByCategory.as_view(), name='category'),  # маршрут класса для модели Category
    # path('news/<int:news_id>/', view_news, name='view_news'),  # маршрут для метода add_news
    path('news/<int:pk>/', ViewNews.as_view(), name='view_news'),  # маршрут для класса ViewNews
    # path('news/add-news/', add_news, name='add_news'),  # маршрут для метода add_news
    path('news/add-news/', CreateNews.as_view(), name='add_news'),  # маршрут для класса CreateNews
]