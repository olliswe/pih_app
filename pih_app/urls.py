from django.urls import path

from . import views

app_name="pih_app"

urlpatterns = [
    path("",views.index,name="index"),
    path("reviewer-dashboard/",views.reviewer_dashboard,name="reviewer_dashboard"),
    path("submit-request/",views.submit_request,name="submit_request"),
    path("submit-request/add-visitors",views.add_visitors, name="add_visitors"),
    path("submit-request/add-flights",views.add_flight_expenses, name="add_flight_expenses"),
    path("submit-request/add-visa",views.add_visa_expenses, name="add_visa_expenses"),
    path("submit-request/add-accommodation",views.add_accommodation_expenses, name="add_accommodation_expenses"),
    path("submit-request/add-transport",views.add_transport_expenses, name="add_transport_expenses"),
    path("submit-request/add-seacoach",views.add_seacoach_expenses, name="add_seacoach_expenses"),
    path("submit-request/add-other",views.add_other_expenses, name="add_other_expenses"),
    path("submit-request/preview",views.preview_submission, name="preview_submission"),
    path("submit-request/success/<int:form_id>",views.submit_request_success, name="submit_request_success"),
    path("personal-dashboard/",views.personal_dashboard, name="personal_dashboard"),
    path("get-requests-json/",views.get_requests_json, name="get_requests_json"),
    path("reviewer-dashboard/pending-review",views.pending_review, name="pending_review"),
    path("reviewer-dashboard/pending-review/<str:alert>/<int:id>",views.pending_review, name="pending_review_alert"),
    path("reviewer-dashboard/review/<int:id>",views.review_request, name="review_request")
]

