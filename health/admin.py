from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Challenge)
admin.site.register(Appointment)
admin.site.register(Supplement)
admin.site.register(Medication)