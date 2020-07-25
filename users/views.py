from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View

from .forms import UserRegistrationForm, UserUpdateForm, ProfileForm
from .utils import EmailVerification

USER = get_user_model()

def register(request):
    if request.method == 'POST':
        u_form = UserRegistrationForm(request.POST)
        p_form = ProfileForm(request.POST)
        if u_form.is_valid() and p_form.is_valid():
            u_form.instance.is_active = False
            user = u_form.save()
            print(user.email)
            p_form.instance.user = user
            p_form.save()
            ev = EmailVerification()
            ev.send_conformation_email(request,user)
            messages.success(request, 'One Final Step. Activate your account by using the link provided in your email.')
            return redirect('users:login')
    else:
        u_form = UserRegistrationForm()
        p_form = ProfileForm()
    return render(request, 'users/register.html', {
        'u_form': u_form,
        'p_form': p_form
    })

class VerificationView(View):
    def get(self, request, uid, token):
        id = EmailVerification().get_user_id(uid)
        user = USER.objects.get(pk=id)
        if user.is_active:
            messages.warning(request, 'Account is already activated')
        else:
            user.is_active = True
            user.save()
            messages.success(request, 'Account successfully activated. Login to continue.')
        return redirect('users:login')

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account was successfully updated.')
            return redirect('users:profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)
