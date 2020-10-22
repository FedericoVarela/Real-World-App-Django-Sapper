from django.contrib import admin
from .models import AppUser

# TODO: remove password from admin

admin.site.register(AppUser)