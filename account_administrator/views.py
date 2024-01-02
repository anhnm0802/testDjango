from .models import *
from account_voting.models import *

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
from account.models import *



# Chọn ngôn ngữ//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
def set_Domain():
        Domain = 'http://127.0.0.1:8000'
        return Domain

def set_Page():
	Page = 2
	return Page

def admin_page(request):
    Domain = set_Domain()
    Number_Account = Account.objects.all()
    Number_Position = Position.objects.all()
    Number_Candidate = Candidate.objects.all()
    Number_Votes = Votes.objects.all()

    chart_data = []
    for i in Number_Position:
        chart_data.append({'name_char':i,'labels':i.candidates.all(),'values':[]})
        print(i.candidates.all())

    for j in chart_data:
        for m in  j['labels']:
            j['values'].append(len(Votes.objects.filter(position=j['name_char'],candidate=m)))

    for k in chart_data:
        k['name_char'] = k['name_char'].name
        aa = []
        for l in k['labels']:
            aa.append(l.fullname)
        k['labels'] = aa


    print('chart_data:',chart_data)

    if request.user.is_authenticated:
        if request.user.is_staff:  # Kiểm tra xem người dùng có thuộc nhóm admin hay không
            context = {'Domain':Domain,'name_account':str(request.user.first_name)+' '+str(request.user.last_name)}
            context['Number_Account'] = Number_Account
            context['Number_Position'] = Number_Position
            context['Number_Candidate'] = Number_Candidate
            context['Number_Votes'] = Number_Votes
            context['chart_data'] = chart_data
            print(context)
            return render(request, 'account_administrator/admin.html', context, status=200)
        else:
            return redirect(reverse('voting_page'))  
    else:
        return redirect(reverse('log_in')) 
    
def admin_voters(request):
    Domain = set_Domain()

    # Kiểm tra xem người dùng đã đăng nhập chưa
    if request.user.is_authenticated:
        if request.user.is_staff:  # Kiểm tra xem người dùng có thuộc nhóm admin hay không
            List_Account = Account.objects.all()
            context = {'Domain':Domain,'List_Account':List_Account,'name_account':str(request.user.first_name)+' '+str(request.user.last_name)}
            print(context)
            return render(request, 'account_administrator/admin_voters.html', context, status=200)
        else:
            return redirect(reverse('voting_page'))  # Chuyển hướng tới trang admin
    else:
        return redirect(reverse('log_in'))  # Chuyển hướng tới trang admin
    
def admin_create_voters(request):
    Page = set_Page()
    Domain = set_Domain()

    # Kiểm tra xem người dùng đã đăng nhập chưa
    if request.user.is_authenticated:
        if request.user.is_staff:  # Kiểm tra xem người dùng có thuộc nhóm admin hay không
            if request.method == 'POST':
                fullname = request.POST.get('fullname')
                photo = request.FILES.get('photo')
                bio = request.POST.get('bio')
                position = request.POST.get('position')
                Candidate.objects.create(fullname=fullname,photo=photo,bio=bio,position=Position.objects.get(pk=position))
                
                # Thực hiện chuyển hướng sau khi thêm bản ghi thành công
                return redirect('admin_create_candidate')

            # Nếu là yêu cầu GET hoặc sau khi chuyển hướng, thực hiện hiển thị danh sách vị trí
            List_Position = Position.objects.all()
            List_Candidate = Candidate.objects.all()
            print('List_Candidate:',List_Candidate)
            context = {'Domain':Domain,'List_Candidate':List_Candidate,'List_Position':List_Position,'name_account':str(request.user.first_name)+' '+str(request.user.last_name)}
            print(context)
            return render(request, 'account_administrator/admin_candidate.html', context, status=200)
        else:
            return redirect(reverse('voting_page'))  # Chuyển hướng tới trang admin
    else:
        return redirect(reverse('log_in'))
        
def admin_update_voters(request):
    Domain = set_Domain()

    # Kiểm tra xem người dùng đã đăng nhập chưa
    if request.user.is_authenticated:
        if request.user.is_staff:  # Kiểm tra xem người dùng có thuộc nhóm admin hay không
            if request.method == 'POST':
                id =  request.POST.get('Editid')
                fullname = request.POST.get('fullname')
                photo = request.FILES.get('photo')
                bio = request.POST.get('bio')
                position = request.POST.get('position')

                pr = Candidate.objects.get(pk=id)

                pr.fullname = fullname
                pr.bio = bio
                pr.position = Position.objects.get(pk=position)
                if photo:
                    pr.photo = photo
                    pr.save()
                pr.save()
                # Thực hiện chuyển hướng sau khi thêm bản ghi thành công
                return redirect('admin_update_candidate')

            # Nếu là yêu cầu GET hoặc sau khi chuyển hướng, thực hiện hiển thị danh sách vị trí
            List_Account = Account.objects.all()
            context = {'Domain':Domain,'List_Account':List_Account,'name_account':str(request.user.first_name)+' '+str(request.user.last_name)}
            print(context)
            return render(request, 'account_administrator/admin_voters.html', context, status=200)
        else:
            return redirect(reverse('voting_page'))  # Chuyển hướng tới trang admin
    else:
        return redirect(reverse('log_in'))
        
def admin_delete_voters(request,id_record):
    Domain = set_Domain()
    print('id_record:',id_record)

    # Kiểm tra xem người dùng đã đăng nhập chưa
    if request.user.is_authenticated:
        if request.user.is_staff:  # Kiểm tra xem người dùng có thuộc nhóm admin hay không
            try:
                pr = Account.objects.get(pk=id_record)
                pr.delete()
            except:
                print('thai')
            List_Account = Account.objects.all()
            context = {'Domain':Domain,'List_Account':List_Account,'name_account':str(request.user.first_name)+' '+str(request.user.last_name)}
            print(context)
            return render(request, 'account_administrator/admin_voters.html', context, status=200)
        else:
            return redirect(reverse('voting_page'))  # Chuyển hướng tới trang admin
    else:
        return redirect(reverse('log_in'))  # Chuyển hướng tới trang admin

                
def admin_positions(request):
    Domain = set_Domain()

    # Kiểm tra xem người dùng đã đăng nhập chưa
    if request.user.is_authenticated:
        if request.user.is_staff:  # Kiểm tra xem người dùng có thuộc nhóm admin hay không
            List_Position = Position.objects.all()
            context = {'Domain':Domain,'List_Position':List_Position,'name_account':str(request.user.first_name)+' '+str(request.user.last_name)}
            print(context)
            return render(request, 'account_administrator/admin_positions.html', context, status=200)
        else:
            return redirect(reverse('voting_page'))  
    else:
        return redirect(reverse('log_in'))  
def admin_create_positions(request):
    Domain = set_Domain()

    # Kiểm tra xem người dùng đã đăng nhập chưa
    if request.user.is_authenticated:
        if request.user.is_staff:  # Kiểm tra xem người dùng có thuộc nhóm admin hay không
            if request.method == 'POST':
                name = request.POST.get('name')
                Position.objects.create(name=name)
                
                # Thực hiện chuyển hướng sau khi thêm bản ghi thành công
                return redirect('admin_create_positions')

            # Nếu là yêu cầu GET hoặc sau khi chuyển hướng, thực hiện hiển thị danh sách vị trí
            List_Position = Position.objects.all()
            context = {'Domain': Domain, 'List_Position': List_Position, 'name_account': str(request.user.first_name) + ' ' + str(request.user.last_name)}
            print(context)
            return render(request, 'account_administrator/admin_positions.html', context, status=200)
        else:
            return redirect(reverse('voting_page'))  # Chuyển hướng tới trang admin
    else:
        return redirect(reverse('log_in'))
        
def admin_update_positions(request):
    Page = set_Page()
    Domain = set_Domain()

    # Kiểm tra xem người dùng đã đăng nhập chưa
    if request.user.is_authenticated:
        if request.user.is_staff:  # Kiểm tra xem người dùng có thuộc nhóm admin hay không
            if request.method == 'POST':
                name = request.POST.get('Editname')
                id =  request.POST.get('Editid')
                pr = Position.objects.get(pk=id)
                pr.name = name
                pr.save()
                # Thực hiện chuyển hướng sau khi thêm bản ghi thành công
                return redirect('admin_update_positions')

            # Nếu là yêu cầu GET hoặc sau khi chuyển hướng, thực hiện hiển thị danh sách vị trí
            List_Position = Position.objects.all()
            context = {'Domain': Domain, 'List_Position': List_Position, 'name_account': str(request.user.first_name) + ' ' + str(request.user.last_name)}
            print(context)
            return render(request, 'account_administrator/admin_positions.html', context, status=200)
        else:
            return redirect(reverse('voting_page'))  # Chuyển hướng tới trang admin
    else:
        return redirect(reverse('log_in'))
        
def admin_delete_positions(request,id_record):
    Domain = set_Domain()
    print('id_record:',id_record)

    # Kiểm tra xem người dùng đã đăng nhập chưa
    if request.user.is_authenticated:
        if request.user.is_staff:  # Kiểm tra xem người dùng có thuộc nhóm admin hay không
            try:
                # name = request.POST.get('name')
                pr = Position.objects.get(pk=id_record)
                pr.delete()
            except:
                print('thai')
            List_Position = Position.objects.all()
            context = {'Domain':Domain,'List_Position':List_Position,'name_account':str(request.user.first_name)+' '+str(request.user.last_name)}
            print(context)
            return render(request, 'account_administrator/admin_positions.html', context, status=200)
        else:
            return redirect(reverse('voting_page'))  # Chuyển hướng tới trang admin
    else:
        return redirect(reverse('log_in'))  # Chuyển hướng tới trang admin
        
def admin_candidate(request):
    Page = set_Page()
    Domain = set_Domain()

    # Kiểm tra xem người dùng đã đăng nhập chưa
    if request.user.is_authenticated:
        if request.user.is_staff:  # Kiểm tra xem người dùng có thuộc nhóm admin hay không
            List_Position = Position.objects.all()
            List_Candidate = Candidate.objects.all()
            print('List_Candidate:',List_Candidate)
            context = {'Domain':Domain,'List_Candidate':List_Candidate,'List_Position':List_Position,'name_account':str(request.user.first_name)+' '+str(request.user.last_name)}
            print(context)
            return render(request, 'account_administrator/admin_candidate.html', context, status=200)
        else:
            return redirect(reverse('voting_page'))  # Chuyển hướng tới trang admin
    else:
        return redirect(reverse('log_in'))  # Chuyển hướng tới trang admin
        
def admin_create_candidate(request):
    Page = set_Page()
    Domain = set_Domain()

    # Kiểm tra xem người dùng đã đăng nhập chưa
    if request.user.is_authenticated:
        if request.user.is_staff:  # Kiểm tra xem người dùng có thuộc nhóm admin hay không
            if request.method == 'POST':
                fullname = request.POST.get('fullname')
                photo = request.FILES.get('photo')
                bio = request.POST.get('bio')
                position = request.POST.getlist('position')
                print('position:',position)
                # Lấy hoặc tạo một ứng viên mới
                candidate = Candidate.objects.create(fullname=fullname,photo=photo,bio=bio)
                candidate.positions.set(position)
                
                # Thực hiện chuyển hướng sau khi thêm bản ghi thành công
                return redirect('admin_create_candidate')

            # Nếu là yêu cầu GET hoặc sau khi chuyển hướng, thực hiện hiển thị danh sách vị trí
            List_Position = Position.objects.all()
            List_Candidate = Candidate.objects.all()
            
            context = {'Domain':Domain,'List_Candidate':List_Candidate,'List_Position':List_Position,'name_account':str(request.user.first_name)+' '+str(request.user.last_name)}
            print(context)
            return render(request, 'account_administrator/admin_candidate.html', context, status=200)
        else:
            return redirect(reverse('voting_page'))  # Chuyển hướng tới trang admin
    else:
        return redirect(reverse('log_in'))
        
def admin_update_candidate(request):
    Domain = set_Domain()

    # Kiểm tra xem người dùng đã đăng nhập chưa
    if request.user.is_authenticated:
        if request.user.is_staff:  # Kiểm tra xem người dùng có thuộc nhóm admin hay không
            if request.method == 'POST':
                id =  request.POST.get('Editid')
                fullname = request.POST.get('fullname')
                photo = request.FILES.get('photo')
                bio = request.POST.get('bio')
                position = request.POST.getlist('position')

                pr = Candidate.objects.get(pk=id)
                pr.fullname = fullname
                pr.bio = bio

                if photo:
                    pr.photo = photo
                    pr.save()
                    pr.positions.set(position)
                pr.save()
                pr.positions.set(position)
                # Thực hiện chuyển hướng sau khi thêm bản ghi thành công
                return redirect('admin_update_candidate')

            # Nếu là yêu cầu GET hoặc sau khi chuyển hướng, thực hiện hiển thị danh sách vị trí
            List_Position = Position.objects.all()
            List_Candidate = Candidate.objects.all()
            print('List_Candidate:',List_Candidate)
            context = {'Domain':Domain,'List_Candidate':List_Candidate,'List_Position':List_Position,'name_account':str(request.user.first_name)+' '+str(request.user.last_name)}
            print(context)
            return render(request, 'account_administrator/admin_candidate.html', context, status=200)
        else:
            return redirect(reverse('voting_page'))  # Chuyển hướng tới trang admin
    else:
        return redirect(reverse('log_in'))
        
def admin_delete_candidate(request,id_record):
    Page = set_Page()
    Domain = set_Domain()
    print('id_record:',id_record)

    # Kiểm tra xem người dùng đã đăng nhập chưa
    if request.user.is_authenticated:
        if request.user.is_staff:  # Kiểm tra xem người dùng có thuộc nhóm admin hay không
            try:
                pr = Candidate.objects.get(pk=id_record)
                pr.delete()
            except:
                print('thai')
            List_Position = Position.objects.all()
            List_Candidate = Candidate.objects.all()
            print('List_Candidate:',List_Candidate)
            context = {'Domain':Domain,'List_Candidate':List_Candidate,'List_Position':List_Position,'name_account':str(request.user.first_name)+' '+str(request.user.last_name)}
            print(context)
            return render(request, 'account_administrator/admin_candidate.html', context, status=200)
        else:
            return redirect(reverse('voting_page'))  # Chuyển hướng tới trang admin
    else:
        return redirect(reverse('log_in'))  # Chuyển hướng tới trang admin
        
def admin_votes(request):
    Page = set_Page()
    Domain = set_Domain()

    # Kiểm tra xem người dùng đã đăng nhập chưa
    if request.user.is_authenticated:
        if request.user.is_staff:  # Kiểm tra xem người dùng có thuộc nhóm admin hay không
            List_Votes = Votes.objects.all()
            print('List_Votes:',List_Votes)
            context = {'Domain':Domain,'List_Votes':List_Votes,'name_account':str(request.user.first_name)+' '+str(request.user.last_name)}
            print(context)
            return render(request, 'account_administrator/admin_votes.html', context, status=200)
        else:
            return redirect(reverse('voting_page'))  # Chuyển hướng tới trang admin
    else:
        return redirect(reverse('log_in'))  # Chuyển hướng tới trang admin