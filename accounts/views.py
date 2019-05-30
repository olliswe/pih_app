from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm





@login_required
def change_password(request):
	if request.method == "POST":
		form = PasswordChangeForm(data = request.POST, user = request.user)
		if form.is_valid():
			form.save()
			update_session_auth_hash(request, form.user)
			return redirect("accounts:change_password_successful")
	else:
		form = PasswordChangeForm(user = request.user)
	return render(request, "registration/password_change_form.html", {"form":form})

@login_required
def change_password_successful(request):
	return render(request, "registration/change_password_success.html")