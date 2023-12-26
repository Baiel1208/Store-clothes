from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from apps.common.views import TitleMixin
from apps.product.models import Basket

from . import forms
from .models import EmailVerification, User


# Create your views here.
class UserLoginView(LoginView, TitleMixin):
    template_name = 'users/login.html'
    form_class = forms.UserLoginForm
    title = 'Store - Авторизация'


class UserRegisterView(TitleMixin, CreateView, SuccessMessageMixin):
    model = User
    form_class = forms.UserRegisterForm 
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')
    success_message = 'Поздравляем! Вы успешно зарегистрировались!'
    title = 'Store - Регистрация'


    def get_context_data(self, **kwargs):
        context = super(UserRegisterView, self).get_context_data()
        context['title'] = 'Store - Регистрация'
        return context


class UserProfileView(TitleMixin, UpdateView):
    model = User
    form_class = forms.UserProfileForm
    template_name = 'users/profile.html'
    title = 'Store - Профиль'


    def get_success_url(self):
        return reverse_lazy('profile', args=(self.object.id, ))


    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data()
        context['title'] = 'Store - Профиль'
        context['baskets'] = Basket.objects.filter(user=self.object)
        return context


class EmailVerificationView(TemplateView, TitleMixin):
    title = 'Store - Подтверждение по элетронной почте'
    template_name = 'users/email_verification.html'


    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(user=user, code=code)
        if email_verifications.exists() and not email_verifications.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get()
        else:
            return HttpResponseRedirect(reverse('index'))


# def logout(request):
#     auth.logout(request)
#     return redirect('index')


# def login(request):
#     if request.method == 'POST':
#         form = forms.UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             user = auth.authenticate(username=username, password=password)
#             if user:
#                 auth.login(request, user)
#                 return redirect('index')
#     else:
#         form = forms.UserLoginForm()
#     context = {'form': form}
#     return render(request, 'users/login.html', context)


# def register(request):
#     if request.method == 'POST':
#         form = forms.UserRegisterForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Поздравляем! Вы успешно зарегистрировались!')
#             return redirect('login')
#     else:
#         form = forms.UserRegisterForm()
#     context = {'form': form}
#     return render(request, 'users/register.html', context)


# @login_required
# def profile(request):
#     if request.method == 'POST':
#         form = forms.UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('profile')
#         else:
#             print(form.errors)
#     else:
#         form = forms.UserProfileForm(instance=request.user)

#     baskets = Basket.objects.filter(user=request.user)

#     context = {'title': 'Store - Профиль',
#                 'form': form,
#                 'baskets': baskets,
#     }
#     return render(request, 'users/profile.html', context)
