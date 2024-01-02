from .models import *

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_list_or_404, get_object_or_404
from django.core.paginator import Paginator


from django.http import HttpResponse
import requests
import time

from django.db import models
from django.utils import timezone

import os

from datetime import datetime

from django.shortcuts import redirect

from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from django.shortcuts import render, redirect, reverse
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from twilio.rest import Client

from django.core.mail import send_mail
from django.conf import settings
import random

# Chọn ngôn ngữ//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
def set_Domain():
	Domain = 'http://127.0.0.1:8000'
	return Domain

def send_sms(email,otp):
    subject = 'Mã xác thực từ hệ thống Bầu Cử'
    message = f'Mã xác thực của bạn là: {otp}'
    email_from = settings.EMAIL_HOST
    send_mail(subject, message, email_from, [email])

def log_in(request):
    Domain = set_Domain()

    # Kiểm tra xem người dùng đã đăng nhập chưa
    if request.user.is_authenticated:
        if request.user.is_staff:  # Kiểm tra xem người dùng có thuộc nhóm admin hay không
            return redirect(reverse('admin_page'))  # Chuyển hướng tới trang admin
        else:
            messages.warning(request, "You are already logged in.")
            return redirect(reverse('voting_page'))  # Chuyển hướng tới trang 'vo'

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Xác thực thông tin đăng nhập
        user = authenticate(request, username=username, password=password)
        if user is not None:
            user = Account.objects.get(username=username)
            print('user:',user)
            print('user.is_staff:',user.is_staff)
            if user.is_staff:  # Kiểm tra xem người dùng có phải là admin không
                login(request, user)
                return redirect(reverse('admin_page'))  # Trang admin
            else:
                if user.accuracy_email:
                    login(request, user)
                    messages.success(request, "Đăng nhập thành công")
                    return redirect(reverse('voting_page'))  # Thay 'home' bằng URL của trang chính của bạn
                else:
                    otp = str(random.randint(100000, 999999))
                    send_sms(user.email,otp)
                    user.otp = otp
                    user.save()
                    context = {'Domain': Domain,'username':username}
                    return redirect(reverse('Accuracy_otp') + f'?email={user.email}')
        else:
            # Đăng nhập thất bại
            messages.error(request, "Đăng nhập thất bại")
            context = {'Domain': Domain}
            return render(request, 'account/log_in.html', context)

    context = {'Domain': Domain}
    return render(request, 'account/log_in.html', context)

def change_password(request):
    Domain = set_Domain()
    context = {'Domain': Domain}

    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        new_password = request.POST.get('new_password')
        otp = request.POST.get('otp')

        print('email:',email)
        print('email:',username)
        print('email:',new_password)
        print('email:',otp)

        if email and not username and not new_password and not otp:
            context['email'] = email
            user = Account.objects.filter(email=email)[0]
            if user:
                username = user.username
                context['username'] = username
                otp = str(random.randint(100000, 999999))
                send_sms(email,otp)
                user.otp = otp
                user.save()
                messages.success(request, "Đã gửi mã xác thực thành công")
            else:
               messages.error(request, "Email không tồn tại") 
        if email and username and not new_password and not otp:
            print('1:',1)
            user = Account.objects.filter(email=email)[0]
            context['username'] = username
            context['email'] = email
            otp = str(random.randint(100000, 999999))
            send_sms(email,otp)
            user.otp = otp
            user.save()
            messages.success(request, "Đã gửi mã xác thực thành công")
        if email and username and new_password and otp:
            print('2:',2)
            user = Account.objects.filter(email=email)[0]
            context['username'] = username
            context['email'] = email
            context['new_password'] = new_password
            context['otp'] = otp
            if user.otp == otp:
                user.set_password(new_password)
                user.save()
                messages.success(request, "Cập nhật mật khẩu thành công tài khoản "+"'"+username+"'")
                return redirect(reverse('log_in'))
            else:
                messages.error(request, "Mã OTP không chính xác")

    return render(request, 'account/reset_password.html', context)


def register(request):
    Domain = set_Domain()
    if request.method == 'POST':
        last_name = request.POST.get('last_name')
        first_name = request.POST.get('first_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        existing_username = Account.objects.filter(username=username)
        existing_email = Account.objects.filter(email=email)

        if existing_username:
            messages.error(request, "Tên đăng nhập '{}' đã tồn tại".format(username))
        elif existing_email:
            messages.error(request, "Địa chỉ email '{}' đã tồn tại".format(email))
        else:
            user = Account.objects.create_user(email=email,username=username, password=password, last_name=last_name, first_name=first_name)
            otp = str(random.randint(100000, 999999))
            send_sms(email,otp)
            user.otp = otp
            user.save()
            context = {'Domain': Domain,'username':username}
            return redirect(reverse('Accuracy_otp') + f'?email={email}')

    # Nếu bạn muốn giữ lại dữ liệu đã nhập trước đó, bạn có thể truyền nó lại trong context
    context = {'Domain': Domain}
    return render(request, 'account/register.html', context, status=200)

def Accuracy_otp(request):
    Domain = set_Domain()
    if request.user.is_authenticated:
        if request.user.is_staff:  # Kiểm tra xem người dùng có thuộc nhóm admin hay không
            return redirect(reverse('admin_page'))  # Chuyển hướng tới trang admin
        else:
            if request.user.accuracy_email:
                messages.success(request, "Đăng nhập thành công")
                return redirect(reverse('voting_page'))  # Thay 'home' bằng URL của trang chính của bạn
            else:
                email = request.GET.get('email')
    else:
        email = request.GET.get('email')
        if request.method == 'POST':
            otp = request.POST.get('otp')
            print('otp:',otp)
            email = request.POST.get('email')
            print('email:',email)
            user = Account.objects.filter(email=email,otp=otp)
            if user:
                user = user[0]
                user.accuracy_email = True
                user.save()
                messages.success(request, "Xác thực thành công tài khoản " +"'"+f'{user.username}'+"'")
                return redirect(reverse('log_in'))
            else:
                messages.error(request, 'Mã xác thực không chính xác')
                return redirect(reverse('Accuracy_otp'))

    # Nếu bạn muốn giữ lại dữ liệu đã nhập trước đó, bạn có thể truyền nó lại trong context
    context = {'Domain': Domain,'email':email}
    return render(request, 'account/accuracy_otp.html', context, status=200)

def resend_code(request):
    Domain = set_Domain()
    context = {'Domain': Domain}
    if request.user.is_authenticated:
        if request.user.is_staff:  # Kiểm tra xem người dùng có thuộc nhóm admin hay không
            return redirect(reverse('admin_page'))  # Chuyển hướng tới trang admin
        else:
            messages.warning(request, "You are already logged in.")
            return redirect(reverse('voting_page'))  # Chuyển hướng tới trang 'vo'
    else:
        if request.method == 'POST':
            email = request.POST.get('email')
            user = Account.objects.get(email=email)
            otp = str(random.randint(100000, 999999))
            send_sms(email,otp)
            user.otp = otp
            user.save()
            messages.success(request, "Đã gửi lại mã xác thực")
            context = {'Domain': Domain,'email':email}
            return redirect(reverse('Accuracy_otp') + f'?email={email}')
    return redirect(reverse('Accuracy_otp'))

def logout_view(request):
    user = request.user
    if user.is_authenticated:
        logout(request)
        for message in list(messages.get_messages(request)):
            if message.tags == messages.SUCCESS:
                messages.get_messages(request).discard(message)
        return redirect(reverse("log_in"))

    return redirect(reverse("log_in"))

