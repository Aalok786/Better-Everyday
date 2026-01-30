from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Habit, DailyEntry, Quote

admin.site.register(Habit)
admin.site.register(DailyEntry)
admin.site.register(Quote)