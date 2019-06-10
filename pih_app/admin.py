from django.contrib import admin
from .models import *

class RequestAdmin(admin.ModelAdmin):
    list_display = ('id','host', 'submission_date')
    list_display_links = ('id','host')
    search_fields = ('host',)
    list_per_page = 25


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('id','type','request_form')
    list_display_links = ('id',)
    list_per_page = 25


class VisitorAdmin(admin.ModelAdmin):
    list_display = ('name','request_form')
    list_display_links = ('name',)
    list_per_page = 25


admin.site.register(Request, RequestAdmin)
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Visitor, VisitorAdmin)



