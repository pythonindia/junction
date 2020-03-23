from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "city",
            "contact_no",
        ]
        exclude = [
            "user",
        ]
