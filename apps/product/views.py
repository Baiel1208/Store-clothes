from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from apps.product import models as m
from apps.users.models import User

# Create your views here.
def index(request):
    context = {'title': 'Магазин'}
    return render(request, 'index.html', context)


def products(request):
    context = {
        'title': 'Магазин Каталог',
        'products': m.Product.objects.all(),
        'categories': m.ProductCategory.objects.all()
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
