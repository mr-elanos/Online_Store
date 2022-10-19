from django.db.models import Q
from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from .models import *
from .forms import ContactForm
from .utils import PagesMixin
from cart.forms import *

menu = [{'title': 'ГОЛОВНА', 'url_name': 'home'},
        {'title': 'НАШІ ПРИЧЕПИ', 'url_name': 'all_categories'},
        {'title': 'ДОСТАВКА І ОПЛАТА', 'url_name': 'buy_and_delivery'},
        {'title': 'КОНТАКТИ', 'url_name': 'contacts'},
        {'title': 'ПРО НАС', 'url_name': 'about'}
        ]


def index(request):
    return render(request, 'pages/index.html', {'menu': menu, 'title': 'Завод автомобільних причепів MAG Trailer'})


class AllCategories(PagesMixin, ListView):
    model = Product
    template_name = 'pages/categories.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Наші причепи')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Product.objects.filter(available=True)


class ShowCategories(PagesMixin, ListView):
    model = Product
    template_name = 'pages/categories.html'
    context_object_name = 'products'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Категорія: ' + str(context['products'][0].category),
                                      cat_selected=context['products'][0].category_id)
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Product.objects.filter(category__slug=self.kwargs['cat_slug'], available=True)


class ShowProduct(PagesMixin, DetailView):
    model = Product
    form_class = CartAddProductForm
    template_name = 'pages/product.html'
    slug_url_kwarg = 'product_slug'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photos'] = ProductImages.objects.filter(product_id=context['product'].id)
        c_def = self.get_user_context(title=context['product'].name)
        return dict(list(context.items()) + list(c_def.items()))


def buy_and_delivery(request):
    return render(request, 'pages/buy_and_delivery.html', {'menu': menu, 'title': 'Доставка і оплата'})


class Contacts(PagesMixin, CreateView):
    form_class = ContactForm
    template_name = 'pages/contacts.html'
    success_url = reverse_lazy('ok_form')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Контакти')
        return dict(list(context.items()) + list(c_def.items()))


class Search(PagesMixin, ListView):
    template_name = 'pages/search_result.html'
    model = Product

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Product.objects.filter(Q(name__icontains=query.lower()) | Q(description__icontains=query.lower())
                                             | Q(name__icontains=query.capitalize())
                                             | Q(description__icontains=query.capitalize()))
        return object_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Результат пошуку')
        return dict(list(context.items()) + list(c_def.items()))


def ok_form(request):
    return render(request, 'pages/ok_form.html', {'menu': menu, 'title': 'Звернення прийнято'})


def about(request):
    return render(request, 'pages/about.html', {'menu': menu, 'title': 'Про підприємство'})


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Сторінка не знайдена :(</h1>')
