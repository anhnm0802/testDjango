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
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
import random


# Chọn ngôn ngữ//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
def set_Domain():
	Domain = 'http://127.0.0.1:8000'
	return Domain

def set_Page():
	Page = 2
	return Page

def send_sms(email,otp):
    subject = 'Mã xác thực từ hệ thống Bầu Cử'
    message = f'Mã xác thực của bạn là: {otp}'
    email_from = settings.EMAIL_HOST
    send_mail(subject, message, email_from, [email])

def voting_page(request):
    Domain = set_Domain()
    
    # Kiểm tra xem người dùng đã đăng nhập chưa
    if request.user.is_authenticated:
        if request.user.is_staff:  # Kiểm tra xem người dùng có thuộc nhóm admin hay không
            return redirect(reverse('admin_page'))  # Chuyển hướng tới trang admin
        else:
            if request.user.accuracy_email:
                List_Position = Position.objects.all()
                # Lấy danh sách vị trí đã vote
                voted_positions = Votes.objects.filter(voter=request.user).values_list('position', flat=True)

                # Loại bỏ các vị trí đã vote khỏi List_Position
                List_Position = List_Position.exclude(id__in=voted_positions)

                print('List_Position :',List_Position)
                context = {'Domain':Domain,'List_Position':List_Position,'name_account':str(request.user.first_name)+' '+str(request.user.last_name)}
                print(context)
                context['User_detail'] = request.user
                return render(request, 'account_voting/voting.html', context, status=200)
            else:
                user = request.user
                otp = str(random.randint(100000, 999999))
                send_sms(request.user.email,otp)
                user.otp = otp
                user.save()
                return redirect(reverse('Accuracy_otp') + f'?email={request.user.email}')
        
def voted_page(request):
    Page = set_Page()
    Domain = set_Domain()

    # Kiểm tra xem người dùng đã đăng nhập chưa
    if request.user.is_authenticated:
        if request.user.is_staff:  # Kiểm tra xem người dùng có thuộc nhóm admin hay không
            return redirect(reverse('admin_page'))  # Chuyển hướng tới trang admin
        else:
            if request.user.accuracy_email:
                pr = Votes.objects.filter(voter=request.user)
                context = {'Domain':Domain,'pr':pr,'name_account':str(request.user.first_name)+' '+str(request.user.last_name)}
                print(context)
                context['User_detail'] = request.user
                return render(request, 'account_voting/voted.html', context, status=200)
            else:
                user = request.user
                otp = str(random.randint(100000, 999999))
                send_sms(request.user.email,otp)
                user.otp = otp
                user.save()
                return redirect(reverse('Accuracy_otp') + f'?email={request.user.email}')
        
def vote_to(request):
    Page = set_Page()
    Domain = set_Domain()

    # Kiểm tra xem người dùng đã đăng nhập chưa
    if request.user.is_authenticated:
        if request.user.is_staff:  # Kiểm tra xem người dùng có thuộc nhóm admin hay không
            return redirect(reverse('admin_page'))  # Chuyển hướng tới trang admin
        else:
            vote_user = Candidate.objects.get(pk=request.GET.get('id_vote_to'))
            position = Position.objects.get(name=request.GET.get('position'))
            print('vote_user:',request.user)
            print('user:',vote_user)
            Votes.objects.create(voter=request.user,candidate=vote_user,position=position)
            return redirect(reverse('voted_page'))


def update_user_account(request):
    Domain = set_Domain()

    # Kiểm tra xem người dùng đã đăng nhập chưa
    if request.user.is_authenticated:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        User = request.user
        User.first_name = first_name
        User.last_name = last_name
        User.save()
        if request.path == '/voting/':
            return redirect(reverse('voting_page'))  # Chuyển hướng tới trang admin
        else:
            return redirect(reverse('voted_page'))
    else:
        return redirect(reverse('log_in'))