import ghasedakpack
import requests
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, reverse
from .forms import LoginForm, OtpLoginForm, CheckOtpForm, AddressCreationForm, RegisterForm
from random import randint
from .models import Otp, User
from django.utils.crypto import get_random_string
from uuid import uuid4

SMS = ghasedakpack.Ghasedak('d38322b3ed7402143c6d40d3789e726d150755998e256f94b9529df86146846f')


def address_add(request):
    form = AddressCreationForm()
    if request.method == 'POST':
        form = AddressCreationForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            next_page = request.GET.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return render(request, 'account/add_address.html', {'form': form})

    return render(request, 'account/add_address.html', {'form': form})


def user_login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            print(cd['username'], cd['password'])
            if user is not None:
                login(request, user)
                return redirect('home:home')
            else:
                form.add_error('username', 'in valid user data')
        else:
            form.add_error('username', 'invalid data')

    return render(request, 'account/login.html', {'form': form})


def otp_login(request):  # OtpLoginView
    form = OtpLoginForm()
    if request.method == 'POST':
        form = OtpLoginForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            randcode = randint(1000, 9999)
            SMS.verification({'receptor': cd["phone"], 'type': '1', 'template': 'randcode', 'param1': randcode})
            token = str(uuid4())
            Otp.objects.create(phone=cd['phone'], code=randcode, token=token)
            print(randcode)
            return redirect(reverse('account:checked') + f'?token={token}')

        else:
            form.add_error('phone', 'in valid user data')

    return render(request, 'account/otp_login.html', {'form': form})


def user_check_cod(request):
    token = request.GET.get('token')
    form = CheckOtpForm()
    if request.method == 'POST':
        form = CheckOtpForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if Otp.objects.filter(code=cd['code'], token=token).exists:
                otp = Otp.objects.get(token=token)
                user, is_create = User.objects.get_or_create(phone=otp.phone)
                login(request, user, backend="django.contrib.auth.backends.ModelBackend")
                otp.delete()
                return redirect('home:home')

    return render(request, 'account/check_code.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home:home')


def user_register(request):
    if request.user.is_anonymous:
        form = RegisterForm()
        if request.method == 'POST':
            form = RegisterForm(data=request.POST)
            if form.is_valid():
                form.save()
                print(request.user)
                return redirect('home:home')
    else:
        return redirect('home:home')
    return render(request, 'account/register.html', {'form': form})





# def user_register(request):
#     user = request.user
#     is_paid = user.is_paid
#     if is_paid:
#         return redirect('home:home')
#     form = RegisterForm(instance=user)
#     if request.method == 'POST':
#         form = RegisterForm(data=request.POST, instance=user)
#         print(form)
#         print(request.POST)
#         if form.is_valid():
#             form.save()
#             user.is_paid = True
#             user.save()
#
#             # login(request, user)
#             return redirect('home:home')
#     return render(request, 'account/register.html', {'form': form})
