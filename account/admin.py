from django.contrib import admin
from django.contrib import auth

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import mark_safe
from .models import *

class Account_Admin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets
    fieldsets[0][1]['fields'] = fieldsets[0][1]['fields'] + (
        'otp','accuracy_email'
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','username', 'password1', 'password2','Cus_name','Cus_birthday','Cus_avatar')}
        ),
    )
    
admin.site.register(Account,Account_Admin)
admin.site.unregister(auth.models.Group)