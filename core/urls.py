from django.contrib import admin
from django.urls import path
# Yahan humne naya function 'create_superuser_view' bhi import kiya hai
from tracker.views import daily_tracker, create_superuser_view, populate_quotes

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', daily_tracker, name='tracker'),
    path('add-quotes/', populate_quotes),
    
    # Ye raha wo Secret Rasta:
    path('make-me-admin/', create_superuser_view),
]