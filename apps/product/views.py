from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.core.cache import cache

from apps.common.views import TitleMixin
from apps.product import models as m


# Create your views here.
class IndexView(TitleMixin, TemplateView):
    template_name = 'index.html'
    title = 'Магазин'


    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data()
        context['title'] = 'Магазин'
        return context

class ProductsListView(TitleMixin, ListView):
    model = m.Product
    template_name = 'products.html'
    paginate_by = 3
    title = 'Магазин Каталог'


    def get_queryset(self):
        queryset = super(ProductsListView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset


    def get_context_data(self, **kwargs):
        context = super(ProductsListView, self).get_context_data()
        context['title'] = 'Магазин Каталог'
        categories = cache.get('categories')
        if not categories:
            context['categories'] = m.ProductCategory.objects.all()
            cache.set('categories', context['categories'], 30)
        else:
            context['categories'] = categories
        return context


@login_required
def basket_add(request, product_id):
    product = m.Product.objects.get(id=product_id)
    baskets = m.Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        m.Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
    
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    basket = m.Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


# def index(request):
#     context = {'title': 'Магазин'}
#     return render(request, 'index.html', context)


# def products(request, category_id=None, page_number=1):
#     products = m.Product.objects.filter(category_id=category_id) if category_id else m.Product.objects.all()
#     per_page = 3
#     paginator = Paginator(products, per_page)
#     products_paginator = paginator.page(page_number)

#     context = {
#         'title': 'Магазин Каталог',
#         'categories': m.ProductCategory.objects.all(),
#         'products': products_paginator,
#     }

#     return render(request, 'products.html', context)