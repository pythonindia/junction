from django.contrib import admin

# Register your models here.
from .models import Profiles


class UserAdmin(admin.ModelAdmin):
	list_display = ('__unicode__','city', 'contact_no')

admin.site.register(Profiles, UserAdmin)
