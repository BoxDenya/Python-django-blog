from django.urls import path
from .views import Home, PostsByCategory, GetPost, PostByTag, Search, register, user_login, user_logout, CreatePost

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('', Home.as_view(), name='home'),
    path('category/<str:slug>/', PostsByCategory.as_view(), name='category'),
    path('tag/<str:slug>/', PostByTag.as_view(), name='tag'),
    path('post/<str:slug>/', GetPost.as_view(), name='post'),
    path('add-post/', CreatePost.as_view(), name='add-post'),
    path('search/', Search.as_view(), name='search'),
]
