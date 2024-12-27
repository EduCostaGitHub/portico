from django import forms
from django.contrib.auth.models import User
from store import models


class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.UserProfile
        fields = '__all__'
        exclude = ('user',)


class UserForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
    )
    password2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Confirm Password'

    )

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = user

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password',
                  'password2', 'email')

    def clean(self, *args, **kwargs):
        data = self.data
        cleaned = self.cleaned_data
        validation_error_msgs = {}

        # check if input user already exists on DB
        # get received data
        data_user = cleaned.get('username')
        data_password = cleaned.get('password')
        data_password2 = cleaned.get('password2')
        data_email = cleaned.get('email')
        # check DB
        db_user = User.objects.filter(username=data_user).first()
        db_email = User.objects.filter(email=data_email).first()
        # error messages
        error_msg_user_exists = 'User already exists'
        error_msg_email_exists = 'Email address already exists'
        error_msg_password_match = 'Passwords do not match'
        error_msg_password_size = 'Passwords must have at least 6 characteres'
        error_msg_required_field = 'This field is required'

        # LOGGED USER - UPDATE
        if self.user:
            if db_user:
                if data_user != db_user.username:
                    validation_error_msgs['username'] = error_msg_user_exists

            if db_email:
                if data_email != db_email.email:
                    validation_error_msgs['email'] = error_msg_email_exists

            if data_password:
                if data_password != data_password2:
                    validation_error_msgs['password'] = error_msg_password_match
                    validation_error_msgs['password2'] = error_msg_password_match

                if len(data_password) < 6:
                    validation_error_msgs['password'] = error_msg_password_size

        # NOT LOGGGED - REGISTER
        else:
            if db_user:
                validation_error_msgs['username'] = error_msg_user_exists

            if db_email:
                validation_error_msgs['email'] = error_msg_email_exists

            if data_password and data_password2:
                if data_password != data_password2:
                    validation_error_msgs['password'] = error_msg_password_match
                    validation_error_msgs['password2'] = error_msg_password_match

                if len(data_password) < 6:
                    validation_error_msgs['password'] = error_msg_password_size
            else:
                validation_error_msgs['password'] = error_msg_required_field
                validation_error_msgs['password2'] = error_msg_required_field

        if validation_error_msgs:
            raise (forms.ValidationError(validation_error_msgs))
