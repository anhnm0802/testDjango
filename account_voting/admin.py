from django.contrib import admin
from .models import *

# Register your models here.

# class Position_Admin(admin.ModelAdmin):
#     list_display = ('name')
#     search_fields = ('name',)

admin.site.register(Position)

# class Candidate_Admin(admin.ModelAdmin):
#     list_display = ('fullname')
#     search_fields = ('fullname',)

admin.site.register(Candidate)

# class Position_Admin(admin.ModelAdmin):
#     list_display = ('catagories_id','catagories_name','Url','Creation_time','Update_time')
#     search_fields = ('catagories_id','Name','Url','Creation_time','Update_time',)

# admin.site.register(Position,Position_Admin)