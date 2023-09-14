from django.contrib import admin
from .models import Train,CustomUser,Booking

# Register your models here.
admin.site.register(Train)
admin.site.register(CustomUser)
admin.site.register(Booking)
