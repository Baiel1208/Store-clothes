from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from apps.product import models as m
from apps.users.models import User

# Create your views here.
def index(request):
    context = {'title': 'Магазин'}
    return render(request, 'index.html', context)


def products(request, category_id=None, page_number=1):
    products = m.Product.objects.filter(category_id=category_id) if category_id else m.Product.objects.all()
    per_page = 3
    paginator = Paginator(products, per_page)
    products_paginator = paginator.page(page_number)

    context = {
        'title': 'Магазин Каталог',
        'categories': m.ProductCategory.objects.all(),
        'products': products_paginator,
    }

    return render(request, 'products.html', context)


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
