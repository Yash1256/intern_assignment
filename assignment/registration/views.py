from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from .forms import UserRegistrationForm
from .models import User


class Register(View):
    def get(self, request):
        return render(request, 'registration/register.html')

    def post(self, request):
        a = UserRegistrationForm(request.POST)
        try:
            if a.is_valid():
                # a.save()
                user = User.objects.create(**dict(a.cleaned_data))
                if user:
                    user.set_password(a.cleaned_data.get('password'))
                    user.save()
                return redirect('login')
            else:
                return render(request, 'registration/register.html', context={'error': a.errors})
        except ValidationError as V:
            return render(request, 'registration/register.html', context={'error': V.message_dict})


class Login(View):
    def get(self, request):
        return render(request, 'registration/login.html')

    def post(self, request):
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)

        if email is None or password is None:
            return render(request, 'registration/login.html', context={'error': 'Fields are required.'})
        u = authenticate(request, email=email, password=password)
        if u is None:
            return render(request, 'registration/login.html', context={'error': 'Email or Password is not valid.'})
        else:
            login(request, u)
            if request.GET.get('next', None):
                return redirect(reverse(request.GET.get('next')))
            else:
                return HttpResponse('TODO')
