from django.contrib import admin
from app.models import CustomUser
from django.contrib.auth.models import User

admin.site.register(CustomUser)
#admin.site.register(User)

# Register your models here.
