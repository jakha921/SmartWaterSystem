from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

from .forms import LoginForm


class UserLoginView(LoginView):
    template_name = 'app/auth-login-basic.html'  # Шаблон страницы входа
    authentication_form = LoginForm  # Класс формы аутентификации

    def get_success_url(self):
        return reverse_lazy('app:tables')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login'
        return context


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('login')  # URL-адрес для перенаправления после успешного выхода
