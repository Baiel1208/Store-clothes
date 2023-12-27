from django.db import models

from apps.users.models import User

# Create your models here.
class Order(models.Model):
    CREATED = 0
    PAID = 1
    ON_WAY = 2
    DELIVERED = 3
    STATUSES = (
        (CREATED, 'Создан'),
        (PAID, 'Оплачен'),
        (ON_WAY, 'В пути'),
        (DELIVERED, 'Доставлен'),
    )


    first_name = models.CharField(max_length=65)
    last_name = models.CharField(max_length=65)
    email = models.EmailField(max_length=255)
    address = models.CharField(max_length=255)
    basket_history = models.JSONField(default=dict)
    created = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(default=CREATED, choices=STATUSES)
    initiator = models.ForeignKey(to=User, on_delete=models.CASCADE)


    def __str__(self):
        return f'Заказ №{self.id}.  {self.first_name}  {self.last_name}'


    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'