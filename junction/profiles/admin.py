from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'contact_no')
    search_fields = ('contact_no', 'city')


admin.site.register(Profile, ProfileAdmin)
