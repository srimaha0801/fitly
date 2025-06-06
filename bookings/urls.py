from django.urls import path
from .views import ClassListView,BookingView,ClientView

urlpatterns = [
    path('classes/',ClassListView.as_view(),name="classlist"),
    path('book/',BookingView.as_view(),name="bookclass"),
    path('bookings/',ClientView.as_view(),name="clientbookings")
]