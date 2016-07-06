from django.contrib import admin

# Register your models here.
from .models import Profile


class UserAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'city', 'contact_no')

admin.site.register(Profile, UserAdmin)
