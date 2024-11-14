from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
'''
class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
'''
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        # Hash the password before saving
        user.password = make_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class EmailVerificationForm(forms.Form):
    verification_code = forms.CharField(
        max_length=4,
        min_length=4,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter 4-digit code'})
    )

