from typing import Any
from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from agenda.models import Contact


class ContactForm(forms.ModelForm):
    picture = forms.ImageField(
        required=False,
        widget=forms.FileInput(
            attrs={
                'accept': 'image/*',
            }
        )
    )

    first_name = forms.CharField(
        help_text='help Text',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Write your first name'
            }
        ),
        label='First Name',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['phone'].widget.attrs.update({
            'placeholder': 'your phone number'
        })

    class Meta:
        model = Contact
        fields = (
            'first_name',
            'last_name',
            'phone',
            'email',
            'description',
            'category',
            'picture',
        )
        widgets = {
            'last_name': forms.TextInput(
                attrs={
                    'placeholder': "Write your last name"
                }
            )
        }

    def clean(self) -> dict[str, Any]:
        cleaned_data = self.cleaned_data
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')

        if first_name == last_name:
            error_msg = ValidationError(
                'first name canot be the same that last name',
                code='invalid',
            )
            self.add_error('first_name', error_msg)
            self.add_error('last_name', error_msg)

        # self.add_error(
        #     'first_name',
        #     ValidationError(
        #         'Mensagem de erro 2',
        #         code='invalid'
        #     )
        # )
        return super().clean()

    def clean_first_name(self):
        data = self.cleaned_data["first_name"]

        if data == 'ABC':
            self.add_error(
                'first_name',
                ValidationError(
                    'Do not input ABC',
                    code='invalid'
                )
            )

        return data


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        required=True,
        min_length=3
    )
    last_name = forms.CharField(
        required=True,
        min_length=3
    )
    email = forms.EmailField()

    class Meta:
        model = User

        fields = (
            'first_name',
            'last_name',
            'email',
            'username',
            'password1',
            'password2',
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            self.add_error(
                'email',
                ValidationError('email já existe', code='invalid')
            )

        return email


class RegisterUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        min_length=2,
        max_length=30,
        required=True,
        help_text='Required',
        error_messages={
            'min_length': 'Please, input more then 2 letters.'
        }
    )

    last_name = forms.CharField(
        min_length=2,
        max_length=30,
        required=True,
        help_text='Required',
    )

    password1 = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
        required=False,
    )

    password2 = forms.CharField(
        label='Confirm Password',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
        required=False,
    )

    class Meta:
        model = User

        fields = (
            'first_name',
            'last_name',
            'email',
            'username',
        )

    def save(self, commit=True):
        cleaned_data = self.cleaned_data
        user = super().save(commit=False)

        password = cleaned_data.get('password1')

        if password:
            user.set_password(password)

        if commit:
            user.save()

        return user

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 or password2:
            if password1 != password2:
                self.add_error(
                    'password2',
                    ValidationError('Password are not equal!')
                )
        return super().clean()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        current_email = self.instance.email

        if current_email != email:
            if User.objects.filter(email=email).exists():
                self.add_error(
                    'email',
                    ValidationError('email já existe', code='invalid')
                )

        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('passwor1')

        if password1:
            try:
                password_validation.validate_password(password1)
            except ValidationError as errors:
                self.add_error(
                    'password1',
                    ValidationError(errors)

                )

        return password1
