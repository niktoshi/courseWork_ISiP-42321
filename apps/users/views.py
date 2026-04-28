from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import LoginForm, ProfileForm, RegisterForm


# Представление login_view обрабатывает вход пользователя на сайт.
def login_view(request):
    if request.user.is_authenticated:
        return redirect('catalog:home')
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.cleaned_data['user'])
        messages.success(request, 'Вы успешно вошли в аккаунт.')
        return redirect('catalog:home')
    return render(request, 'login.html', {'form': form})


# Функция register_view 
def register_view(request):
    if request.user.is_authenticated:
        return redirect('catalog:home')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Аккаунт создан.')
        return redirect('catalog:home')
    return render(request, 'register.html', {'form': form})


@login_required
# Функция profile_view 
def profile_view(request):
    form = ProfileForm(request.POST or None, instance=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Профиль обновлён.')
        return redirect('users:profile')
    return render(request, 'profile.html', {
        'form': form,
        'orders': request.user.orders.all()[:5],
    })


# Представление logout_view завершает сессию пользователя.
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.info(request, 'Вы вышли из аккаунта.')
    return redirect('catalog:home')
