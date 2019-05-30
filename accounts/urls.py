from django.urls import path
from accounts import views

app_name = "accounts"

urlpatterns =[
    path('change-password/',views.change_password,name="change_password"),
    path('change-password-success/',views.change_password_successful,name="change_password_successful")
]

