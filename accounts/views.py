from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from PIL import Image
from . import forms
from . import models
from . import images


def sign_in(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            if form.user_cache is not None:
                user = form.user_cache
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(
                        reverse('accounts:profile')  # TODO: go to profile
                    )
                else:
                    messages.error(
                        request,
                        "That user account has been disabled."
                    )
            else:
                messages.error(
                    request,
                    "Username or password is incorrect."
                )
    return render(request, 'accounts/sign_in.html', {'form': form})


def sign_up(request):
    form = forms.CreationForm()
    if request.method == 'POST':
        form = forms.CreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            login(request, user)
            messages.success(
                request,
                "You're now a user! You've been signed in, too."
            )
            return HttpResponseRedirect(reverse('accounts:profile'))  # TODO: go to profile
    return render(request, 'accounts/sign_up.html', {'form': form})


def sign_out(request):
    logout(request)
    messages.success(request, "You've been signed out. Come back soon!")
    return HttpResponseRedirect(reverse('home'))


@login_required
def profile_view(request):
    pk = request.user.pk
    profile = get_object_or_404(models.Profile, pk=pk)
    image_file = images.image_filename(pk)
    return render(request, 'accounts/profile_view.html',
                  {'profile':profile, 'image':image_file})


@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = forms.UpdateUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your Profile has been updated")
            return HttpResponseRedirect(reverse('accounts:profile'))
    else:
        profile = get_object_or_404(models.Profile, pk=request.user.pk)
        form = forms.UpdateUserForm(instance=profile)
    return render(request, 'accounts/profile_edit.html', {'form':form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password has been changed')
            return HttpResponseRedirect(reverse('accounts:profile'))
        else:
            messages.error(request, 'Please correct the error below')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {'form':form})
