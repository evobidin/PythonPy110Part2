from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from logic.services import add_user_to_cart, add_user_to_wishlist
from django.views import View
from .forms import CustomUserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


def login_view(request):
    if request.method == "GET":
        return render(request, "login/login.html")

    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            add_user_to_cart(request, user.username)
            add_user_to_wishlist(request, user.username)
            return redirect("/")
        return render(request, "login/login.html", context={"error": "Неверные данные"})


def logout_view(request):
    if request.method == "GET":
        logout(request)
        return redirect("/")


class SignUpView(View):
    def get(self, request):
        return render(request, "login/signup.html")

    def post(self, request):
        form = CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = User.objects.create_user(username=username, email=email,
                                            password=password)
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')  # Авторизируем пользователя
            return redirect('/')
        return render(request, "login/signup.html",
                      context={'errors': form.errors})
