from django.views.generic.edit import CreateView


from apps.orders.forms import OrderForm


# Create your views here.
class OrderCreateView(CreateView):
    template_name = 'orders/order-create.html'
    form_class = OrderForm
