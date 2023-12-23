from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from apps.product.models import Product, ProductCategory


# Create your tests here.
class IndexViewTestCase(TestCase):
    def test_view(self):
        path = reverse('index')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Магазин')
        self.assertTemplateUsed(response, 'index.html')


class ProductsListViewTestCase(TestCase):
    fixtures = ['categories.json', 'goods.json']

    def setUp(self) -> None:
        self.products = Product.objects.all()


    def test_list(self):
        path = reverse('products')
        response = self.client.get(path)

        self._common_tests(response)
        self.assertEqual(list(response.context_data['object_list']), list(self.products[:3]))


    def test_list_with_category(self):
        category = ProductCategory.objects.first()
        path = reverse('category', kwargs={'category_id': category.id})
        response = self.client.get(path)

        self._common_tests(response)
        self.assertEqual(
            list(response.context_data['object_list']),
            list(self.products.filter(category_id=category.id))
        )


    def _common_tests(self, response):
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Магазин Каталог')
        self.assertTemplateUsed(response, 'products.html')