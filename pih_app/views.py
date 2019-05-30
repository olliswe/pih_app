from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from accounts.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from accounts.decorators import reviewer_required



@login_required
def index(request):
    id = request.user.id
    user = User.objects.get(id=id)
    if user.is_reviewer:
        return redirect("pih_app:reviewer_dashboard")
    else:
        return redirect("pih_app:submit_request")

@login_required
@reviewer_required
def reviewer_dashboard(request):
    return render(request,"pih_app/reviewer-dashboard.html")


@login_required
def submit_request(request):
    return render(request,"pih_app/submit-request.html")