from django.shortcuts import render
from django.views import View
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    success_url = 'app/index.html'


class UserProfileView(LoginRequiredMixin, View):
    template_name = 'users/profile.html'

