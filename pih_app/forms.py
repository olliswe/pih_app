from django import forms
from .models import *



class RequestForm(forms.ModelForm):

    class Meta:

        model = Request

        fields = ['num_visitors','departure_place', 'other_place','purpose','arrival_date','departure_date']


class VisitorForm(forms.ModelForm):

    class Meta:

        model = Visitor

        exclude = ['request_form']



class ExpenseForm(forms.ModelForm):

    class Meta:

        model = Expense

        exclude = ['request_form','type']


class ReviewForm(forms.ModelForm):

    class Meta:

        model = Request

        fields = ['status','review_comment']