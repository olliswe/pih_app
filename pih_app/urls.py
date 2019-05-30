from django.urls import path

from . import views

app_name="pih_app"

urlpatterns = [
    path("",views.index,name="index"),
    path("dashboard/",views.reviewer_dashboard,name="reviewer_dashboard"),
    path("submit-request/",views.submit_request,name="submit_request")
]

