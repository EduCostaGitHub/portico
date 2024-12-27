
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.list import ListView
from django.contrib import messages
from django.views import View
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import copy

from store import models
from store import forms


# Create your views here.
class BaseProfile(View):
    template_name = 'store/profile/create.html'

    def setup(self, *args, **kwargs) -> None:
        super().setup(*args, **kwargs)

        self.cart = copy.deepcopy(self.request.session.get('cart', {}))

        self.profile = None

        if self.request.user.is_authenticated:
            self.profile = models.UserProfile.objects.filter(
                user=self.request.user
            ).first()

            self.context = {
                'userform': forms.UserForm(
                    data=self.request.POST or None,
                    user=self.request.user,
                    instance=self.request.user,
                ),
                'profileform': forms.ProfileForm(
                    data=self.request.POST or None,
                    instance=self.profile,
                ),
            }
        else:
            self.context = {
                'userform': forms.UserForm(
                    data=self.request.POST or None
                ),
                'profileform': forms.ProfileForm(
                    data=self.request.POST or None
                ),
            }

        self.userform = self.context['userform']
        self.profileform = self.context['profileform']

        if self.request.user.is_authenticated:
            self.template_name = 'store/profile/update.html'

        self.render = render(self.request, self.template_name, self.context)

    def get(self, *args, **kwargs):
        return self.render


class CreateProfile(BaseProfile):
    def post(self, *args, **kwargs):

        _authentic = None

        if not self.userform.is_valid() or not self.profileform.is_valid():
            messages.error(
                self.request,
                'Please verify form data',
            )
            return self.render

        username = self.userform.cleaned_data.get('username')
        password = self.userform.cleaned_data.get('password')
        email = self.userform.cleaned_data.get('email')
        first_name = self.userform.cleaned_data.get('first_name')
        last_name = self.userform.cleaned_data.get('last_name')

        # user is logged
        if self.request.user.is_authenticated:
            _user = get_object_or_404(
                User, username=self.request.user.username)  # type: ignore
            _user.username = username

            if password:
                _user.set_password(password)

            _user.email = email
            _user.first_name = first_name
            _user.last_name = last_name

            _user.save()

            if not self.profile:
                self.profileform.cleaned_data['user'] = _user
                _profile = models.UserProfile(**self.profileform.cleaned_data)
                _profile.save()
            else:
                _profile = self.profileform.save(commit=False)
                _profile.user = _user
                _profile.save()

        # user is NOT LOGGED
        else:
            # save user
            _user = self.userform.save(commit=False)
            _user.set_password(password)
            _user.save()
            # save profile
            _profile = self.profileform.save(commit=False)
            _profile.user = _user
            _profile.save()

        if password:
            _authentic = authenticate(
                self.request,
                username=_user,
                password=password,
            )

        if _authentic:
            login(self.request, user=_user)

        self.request.session['cart'] = self.cart
        self.request.session.save()

        messages.success(
            self.request,
            'Your profile is update/created'
        )

        return redirect('store:profile_create')
        # return self.render


class UpdateProfile(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Update Profile')


class LoginProfile(View):
    def post(self, *args, **kwargs):
        _username = self.request.POST.get('username')
        _password = self.request.POST.get('password')

        if not _username or not _password:
            messages.error(
                self.request,
                'Please input username and password',
            )
            return redirect('store:profile_create')

        # authenticate user
        _user = authenticate(
            self.request,
            username=_username,
            password=_password,
        )

        if not _user:
            messages.error(
                self.request,
                'Please input correct username and password',
            )
            return redirect('store:profile_create')

        login(
            self.request,
            user=_user,
        )

        messages.success(
            self.request,
            'Welcome, you are logged',
        )
        return redirect('store:cart')


class LogoutProfile(View):
    def get(self, *args, **kwargs):
        # capy cart
        cart = copy.deepcopy(self.request.session.get('cart', {}))
        # logout
        logout(self.request)
        # paste cart to session
        self.request.session['cart'] = cart
        self.request.session.save()

        messages.success(
            self.request,
            'Good bye, you logged out',
        )
        return redirect('store:list')
