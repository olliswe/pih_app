from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from accounts.models import User
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from accounts.decorators import reviewer_required
from django.forms import formset_factory
from .forms import RequestForm, VisitorForm, ExpenseForm, ReviewForm
from .models import *
from django.utils.timesince import timesince
from django.utils import timezone



@login_required
def index(request):
    id = request.user.id
    user = User.objects.get(id=id)
    if user.is_reviewer:
        return redirect("pih_app:reviewer_dashboard")
    else:
        return redirect("pih_app:personal_dashboard")


@login_required
@reviewer_required
def reviewer_dashboard(request):
    requests_under_review = Request.objects.filter(status = 'review').exclude(host = request.user )
    approved_requests = Request.objects.filter(status = 'approved')
    outstanding_expenses = Expense.manager.outstanding()
    expenses_need_reimbursement = Expense.manager.need_reimbursement()

    return render(request,"pih_app/reviewer-dashboard.html",{"requests_under_review":requests_under_review,
                                                             "approved_requests":approved_requests,
                                                             "outstanding_expenses":outstanding_expenses,
                                                             "expenses_need_reimbursement":expenses_need_reimbursement
                                                             })

@login_required
def personal_dashboard(request):
    requests_pending_review = Request.objects.filter(status = 'review', host = request.user)
    approved_requests = Request.objects.filter(status='approved', host=request.user)
    rejected_requests = Request.objects.filter(status='rejected', host=request.user)
    items_need_organizing = Expense.manager.need_organizing().filter(name_of_organizer=request.user)
    return render(request,"pih_app/personal-dashboard.html", {'requests_pending_review':requests_pending_review,
                                                              'approved_requests':approved_requests,
                                                              'rejected_requests':rejected_requests,
                                                              'items_need_organizing':items_need_organizing
                                                              })



@login_required
def submit_request(request):


    if request.method =='POST':
        form = RequestForm(request.POST)

        if form.is_valid():
            request.session['request_form_data']=form.cleaned_data
            return HttpResponseRedirect(reverse('pih_app:add_visitors'))

    else:
        form = RequestForm()

    return render(request,'pih_app/submit-request.html',{'form':form})




@login_required
def add_visitors(request,):
    #Visitors Form (leads on to adding expenses)
    request_form_data = request.session['request_form_data']
    number_of_visitors = request_form_data['num_visitors']
    VisitorFormSet = formset_factory(VisitorForm, extra=number_of_visitors, max_num=number_of_visitors, min_num=number_of_visitors, validate_min=True)

    if request.method == 'POST':
        visitor_formset = VisitorFormSet(request.POST)

        if visitor_formset.is_valid():
            request.session['visitor_data']=visitor_formset.cleaned_data
            return HttpResponseRedirect(reverse('pih_app:add_flight_expenses'))

    else:
        visitor_formset = VisitorFormSet()

    return render(request,'pih_app/add-visitors.html',{'formset':visitor_formset, 'num_visitors':number_of_visitors})


@login_required
def add_flight_expenses(request,):
    #expenses form
    if request.method == 'POST':
        form = ExpenseForm(request.POST)

        if form.is_valid():
            expense = form.cleaned_data
            expense['type'] = 'Flights'
            request.session['flights']=expense

            return HttpResponseRedirect(reverse('pih_app:add_visa_expenses'))

    else:
        form = ExpenseForm()
    return render(request, 'pih_app/expenses/flights.html', {'form': form})

@login_required
def add_visa_expenses(request,):
    #expenses form
    if request.method == 'POST':
        form = ExpenseForm(request.POST)

        if form.is_valid():
            expense = form.cleaned_data
            expense['type'] = 'Visa'
            request.session['visa']=expense

            return HttpResponseRedirect(reverse('pih_app:add_accommodation_expenses'))

    else:
        form = ExpenseForm()
    return render(request, 'pih_app/expenses/visa.html', {'form': form})


@login_required
def add_accommodation_expenses(request,):
    #expenses form
    if request.method == 'POST':
        form = ExpenseForm(request.POST)

        if form.is_valid():
            expense = form.cleaned_data
            expense['type'] = 'Accommodation'
            request.session['accommodation']=expense

            return HttpResponseRedirect(reverse('pih_app:add_transport_expenses'))

    else:
        form = ExpenseForm()
    return render(request, 'pih_app/expenses/accommodation.html', {'form': form})


@login_required
def add_transport_expenses(request,):
    #expenses form
    if request.method == 'POST':
        form = ExpenseForm(request.POST)

        if form.is_valid():
            expense = form.cleaned_data
            expense['type'] = 'Transport'
            request.session['transport']=expense

            return HttpResponseRedirect(reverse('pih_app:add_seacoach_expenses'))

    else:
        form = ExpenseForm()
    return render(request, 'pih_app/expenses/transport.html', {'form': form})


@login_required
def add_seacoach_expenses(request,):
    #expenses form
    if request.method == 'POST':
        form = ExpenseForm(request.POST)

        if form.is_valid():
            expense = form.cleaned_data
            expense['type'] = 'Seacoach'
            request.session['seacoach']=expense

            return HttpResponseRedirect(reverse('pih_app:add_other_expenses'))

    else:
        form = ExpenseForm()
    return render(request, 'pih_app/expenses/seacoach.html', {'form': form})


@login_required
def add_other_expenses(request,):
    #expenses form
    if request.method == 'POST':
        form = ExpenseForm(request.POST)

        if form.is_valid():
            expense = form.cleaned_data
            expense['type'] = 'Other'
            request.session['other']=expense

            return HttpResponseRedirect(reverse('pih_app:preview_submission'))

    else:
        form = ExpenseForm()
    return render(request, 'pih_app/expenses/other.html', {'form': form})


@login_required
def preview_submission(request,):
    if request.method == 'POST':

        request_form_data = request.session['request_form_data']
        request_object = Request.objects.create(
            host=request.user,
            departure_place=request_form_data['departure_place'],
            other_place=request_form_data['other_place'],
            purpose=request_form_data['purpose'],
            arrival_date=request_form_data['arrival_date'],
            departure_date=request_form_data['departure_date'],
            num_visitors=request_form_data['num_visitors'],
        )

        visitor_form_data = request.session['visitor_data']
        for visitor_data in visitor_form_data:
            Visitor.objects.create(
                name=visitor_data['name'],
                request_form=request_object
            )

        for expense_type in ['flights','visa','accommodation','transport','seacoach']:
            expense = request.session[expense_type]
            Expense.objects.create(
                type = expense['type'],
                organized_by_us=expense['organized_by_us'],
                name_of_organizer=expense['name_of_organizer'] ,
                expenses_covered_by=expense['expenses_covered_by'],
                expenses_amount = expense['expenses_amount'],
                notes = expense['notes'],
                request_form=request_object
            )
            del request.session[expense_type]

        try:
            expense = request.session['other']
            Expense.objects.create(
                type=expense['type'],
                organized_by_us=expense['organized_by_us'],
                name_of_organizer=expense['name_of_organizer'],
                expenses_covered_by=expense['expenses_covered_by'],
                expenses_amount=expense['expenses_amount'],
                notes=expense['notes'],
                request_form=request_object
            )
            del request.session['other']
        finally:
            return HttpResponseRedirect(reverse('pih_app:submit_request_success',kwargs = {'form_id':request_object.id}))

    else:
        return render(request, 'pih_app/preview.html',)


@login_required
def submit_request_success(request, form_id):
    request_form = get_object_or_404(Request,id=form_id)
    return render(request, "pih_app/submit-request-success.html",{'request_form':request_form})


@login_required
@reviewer_required
def pending_review(request, alert=None, id=None):
    return render(request, "pih_app/reviewer/pending-review.html",{"alert":alert,"id":id})



@login_required
@reviewer_required
def review_request(request, id):
    request_form = get_object_or_404(Request, id=id)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance = request_form)

        if form.is_valid():
            data = form.save(commit=False)
            data.review_date = timezone.now()
            data.reviewer = request.user
            data.save()
            if form.cleaned_data['status']=='approved':
                id = request_form.id
                return HttpResponseRedirect(reverse("pih_app:pending_review_alert",kwargs={"alert":'approved',"id":id}))
            else:
                id = request_form.id
                return HttpResponseRedirect(reverse("pih_app:pending_review_alert", kwargs={"alert": 'rejected', "id": id}))

    else:
        form = ReviewForm(instance = request_form)

    return render(request,"pih_app/reviewer/review-form.html",{"form":form, "r":request_form})


@login_required
def get_requests_json(request):
    if request.GET.get('type')=='awaiting review':
        requests = Request.objects.filter(status = 'review').exclude(host = request.user)
    elif request.GET.get('type')=='approved':
        requests = Request.objects.filter(status='approved')
    else:
        requests = Request.objects.all()
    requests_json = []
    for request_form in requests:
        visitors = ''
        count = 1
        for visitor in request_form.visitor_set.all():
            if count > 3:
                visitors += ', +'+str(request_form.num_visitors-(count-1)) +" more"
                break
            elif count==1:
                visitors += visitor.name
                count += 1
            else:
                visitors += ', '+visitor.name
                count += 1

        requests_json.append(
            {
                'ID':request_form.id,
                'Submission Date':str(timesince(request_form.submission_date)).split(",")[0]+' ago',
                'Status':request_form.status,
                'Host':request_form.host.__str__(),
                '# of Visitors':request_form.num_visitors,
                'Visitor Name(s)': visitors,
                'Arrival Date':request_form.arrival_date.strftime("%d %B %Y"),
                'Departure Date':request_form.departure_date.strftime("%d %B %Y")
            }
        )

    return JsonResponse(requests_json, safe=False)