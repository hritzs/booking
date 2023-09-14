from django.urls import path
from . import views

urlpatterns = [
    path('api/signup', views.register_user, name='register-user'),
    path('api/login', views.CustomObtainAuthToken.as_view(), name='login-user'),
    path('api/trains/create', views.create_train, name='create-train'),
    path('api/trains/availability', views.get_seat_availability, name='get-seat-availability'),
    path('api/trains/<int:train_id>/book', views.book_seat, name='book-seat'),
    path('api/bookings/<int:booking_id>', views.get_booking_details, name='get-booking-details'),
]
