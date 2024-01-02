"""th URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
# from Data_Interaction.admin import admin_site
from django.urls import path

from account.views import *
from account_voting.views import *
from account_administrator.views import *
from rest_framework.routers import DefaultRouter,SimpleRouter
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

from django.urls import re_path,path


from django.views.generic.base import TemplateView
from django.conf.urls.static import serve

from django.views.generic import RedirectView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/login/',log_in,name='log_in'),
    path('account/register/',register,name='register'),
    path('account/accuracy-otp/',Accuracy_otp,name='Accuracy_otp'),
    path('logout/', logout_view, name='logout_view'),
    path('change-password/',change_password,name='change_password'),
    path('update-user-account/',update_user_account,name='update_user_account'),

    # Trang bầu chọn
    path('voting/',voting_page,name='voting_page'),
    path('voted/',voted_page,name='voted_page'),
    path('vote-to/',vote_to,name='vote_to'),
    path('resend-code/',resend_code,name='resend_code'),

    # Trang người đi bầu
    path('administrator/voters/',admin_voters,name='admin_voters'),
    path('administrator/voters/create',admin_create_voters,name='admin_create_voters'),
    path('administrator/voters/update',admin_update_voters,name='admin_update_voters'),
    path('administrator/voters/delete/<int:id_record>/', admin_delete_voters,name='admin_delete_voters'),
    #Trang vị trí
    path('administrator/',admin_page,name='admin_page'),
    path('administrator/positions/',admin_positions,name='admin_positions'),
    path('administrator/positions/create',admin_create_positions,name='admin_create_positions'),
    path('administrator/positions/update',admin_update_positions,name='admin_update_positions'),
    path('administrator/positions/delete/<int:id_record>/', admin_delete_positions,name='admin_delete_positions'),
    # Trang ứng viên
    path('administrator/candidate/',admin_candidate,name='admin_candidate'),
    path('administrator/candidate/create',admin_create_candidate,name='admin_create_candidate'),
    path('administrator/candidate/update',admin_update_candidate,name='admin_update_candidate'),
    path('administrator/candidate/delete/<int:id_record>/', admin_delete_candidate,name='admin_delete_candidate'),

    path('administrator/votes/',admin_votes,name='admin_votes'),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)