
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ServiceRequest


class CitizenRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text="Enter a valid email address.",
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()

        return user




class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = [
            "category",
            "title",
            "description",
            "location",
            "image",
        ]
        widgets = {
            "description": forms.Textarea(
                attrs={
                    "rows": 5,
                    "placeholder": "Describe the issue clearly...",
                }
            ),
            "location": forms.TextInput(
                attrs={
                    "placeholder": "Estate, village, road or landmark",
                }
            ),
            "title": forms.TextInput(
                attrs={
                    "placeholder": "Briefly describe the issue",
                }
            ),
        }
