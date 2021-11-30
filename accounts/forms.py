from django.contrib.auth import get_user_model
from django import forms
from django.core.exceptions import ObjectDoesNotExist


User = get_user_model()


class RegisterForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "user-password"
            }
        )
    )
    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "user-confirm-password"
            }
        )
    )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        qs = User.objects.filter(username__iexact=username)
        if qs.exists():
            raise forms.ValidationError("This is an invalid username, please pick another.")
        return username

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if not (password and confirm_password):
            raise forms.ValidationError("You must confirm your password")
        elif password != confirm_password:
            raise forms.ValidationError("Your passwords do not match")
        return password


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            "class": "form-control"
        }))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "user-password"
            }
        )
    )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        qs = User.objects.filter(username__iexact=username)
        if qs.count() != 1:
            raise forms.ValidationError("Username not found.")
        return username

    def clean_password(self):
        password = self.cleaned_data.get("password")
        try:
            user = User.objects.get(username__iexact=self.cleaned_data.get("username"))
        except ObjectDoesNotExist:
            return ""
        if not user.check_password(password):
            raise forms.ValidationError("The password you entered is incorrect")
        return password
