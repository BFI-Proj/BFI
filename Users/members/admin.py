from django.contrib import admin
from .models import UserProfile
from .models import FoodItem
from .models import Appointment

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(FoodItem)
admin.site.register(Appointment)

