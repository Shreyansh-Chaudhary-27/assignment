from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class SignupForm(forms.ModelForm):
    user_type = forms.ChoiceField(choices=UserProfile.USER_TYPE_CHOICES)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    profile_picture = forms.ImageField(required=False)
    address_line1 = forms.CharField()
    city = forms.CharField()
    state = forms.CharField()
    pincode = forms.CharField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password") != cleaned_data.get("confirm_password"):
            raise forms.ValidationError("Passwords do not match.")
