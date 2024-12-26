from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render

from agenda.forms import RegisterForm, RegisterUpdateForm


def register(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'User Registered')
            return redirect('agenda:index')

    return render(
        request,
        'agenda/pages/register.html',
        {
            'form': form
        }
    )


@login_required(login_url='agenda:login')
def user_update(request):
    form = RegisterUpdateForm(instance=request.user)

    if request.method != 'POST':
        return render(
            request,
            'agenda/pages/user_update.html',
            {
                'form': form
            }
        )
    # POST
    form = RegisterUpdateForm(data=request.POST, instance=request.user)

    if not form.is_valid():
        return render(
            request,
            'agenda/pages/user_update.html',
            {
                'form': form
            }
        )

    # Update
    form.save()
    return redirect('agenda:user_update')


def login_view(request):
    form = AuthenticationForm(request)

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            # login
            auth.login(request, user)
            messages.success(request, 'You Logged in')
            # print(user)
            return redirect('agenda:index')

        messages.error(request, 'Invalid Login')

    return render(
        request,
        'agenda/pages/login.html',
        {
            'form': form
        }
    )


@login_required(login_url='agenda:login')
def logout_view(request):
    auth.logout(request)
    return redirect('agenda:login')
