from django.contrib.auth import login, logout
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.paginator import Paginator

from .utils import MyMixin

from .models import News, Category
from .forms import NewsForm, UserRegisterForm, UserLoginForm, ContactForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.mail import send_mail

def user_logout(request):
    logout(request)
    return redirect('login')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'news/register.html', {"form": form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'news/login.html', {"form": form})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['content'], 'ras_deadman@mail.ru', ['d.levdanskiy@gmail.com'], fail_silently=True)
            if mail:
                messages.success(request, 'Письмо отправлено')
                return redirect('contact')
            else:
                messages.error(request, 'Ошибка отправки')
        else:
            messages.error(request, 'Ошибка валидации')
    else:
        form = ContactForm()
    return render(request, 'news/test1.html', {"form": form})

def test(request):
    objects = ['john1', 'paul2', 'george3', 'ringo4', 'john5', 'paul6', 'george7']
    paginator = Paginator(objects, 2)
    page_num = request.GET.get('page', 1)
    page_objects = paginator.get_page(page_num)
    return render(request, 'news/test.html', {'page_obj': page_objects})


class HomeNews(MyMixin, ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    # extra_context = {'title': 'Главная страница'}
    # queryset = News.objects.select_related('category')
    mixin_prop = 'hello world'
    paginate_by = 2

    # переопределяем метод get_context_data
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  # сохраняем все пораметры метода, чтобы не затереть
        context['title'] = self.get_upper('Главная страница')
        context['mixin_prop'] = self.get_prop()
        return context

    # метод для фильтрации данных ( если категория не опубликованна выводится не будет на главной странице )
    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')
    #  select_related загружает категории не отложенно, а сразу

# def index(request):
#     news = News.objects.all()
#     # categories = Category.objects.all()
#     context = {
#         'news': news,
#         'title': 'Список новостей',
#         # 'categories': categories,
#     }
#     return render(request, template_name='news/index.html', context=context)

class NewsByCategory(MyMixin, ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    allow_empty = False  # Если категории нет будет ошибка 404 вместо Doesn't exists
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  # сохраняем все пораметры метода, чтобы не затереть
        context['title'] = self.get_upper(Category.objects.get(pk=self.kwargs['category_id']))
        return context

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category')

# def get_category(request, category_id):
#     news = News.objects.filter(category_id=category_id)
#     # categories = Category.objects.all()
#     category = Category.objects.get(pk=category_id)
#     return render(request, 'news/category.html', {'news': news, 'category': category})

class ViewNews(DetailView):
    model = News
    context_object_name = 'news_item'
    # template_name = 'news/news_detail.html'
    # pk_url_kwarg = 'news_id'

# def view_news(request, news_id):
#     # news_item = News.objects.get(pk=news_id)
#     news_item = get_object_or_404(News, pk=news_id)
#     return render(request, 'news/view_news.html', {"news_item": news_item})


# Метод для несвязанной формы с моделью
# def add_news(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST)  # Форма связана с данными
#         if form.is_valid():
#             # print(form.cleaned_data)
#             news = News.objects.create(**form.cleaned_data)  # Сохраняем данные из формы
#             return redirect(news)
#     else:
#         form = NewsForm()  # Форма не связана с данными
#     return render(request, 'news/add_news.html', {'form': form})


class CreateNews(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    # success_url = reverse_lazy('home')  # редирект на главную страницу
    # login_url = '/admin/'
    raise_exception = True

# def add_news(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST)  # Форма связана с данными
#         if form.is_valid():
#             # print(form.cleaned_data)
#             news = form.save()
#             return redirect(news)
#     else:
#         form = NewsForm()  # Форма не связана с данными
#     return render(request, 'news/add_news.html', {'form': form})