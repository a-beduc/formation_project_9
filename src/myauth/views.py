from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect, render
from . import forms
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


class LogoutView(View, LoginRequiredMixin):
    redirect_field_name = settings.LOGOUT_REDIRECT_URL

    def get(self, request):
        logout(request)
        return redirect(self.redirect_field_name)


class LoginView(View):
    template_name = 'myauth/login.html'
    form_class = forms.LoginForm

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        form = self.form_class()
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(
                    request,
                    message="Nom d'utilisateur ou mot de passe incorrect.")
        return render(request, self.template_name, context={'form': form})


class SignupView(View):
    template_name = 'myauth/signup.html'
    form_class = forms.SignupForm

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        form = self.form_class()
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
        return render(request, self.template_name, context={'form': form})
