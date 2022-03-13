from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import Register_form
from django.contrib.auth.decorators import login_required
from .models import Profile
from core.models import Connection_Spec

# Create your views here.

def register(request):
    # register functionality does not require a model - only a (custom) form
    if request.method == 'POST':
        form = Register_form(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Welcome {username}! Your account was created.')
            return redirect('login')
    else:
        form = Register_form()
    return render(request, 'user_app/register.html', {'form':form})


def login_page(request):
    return render(request, 'user_app/login.html')


# restrict access with a decorator
@login_required
def profile_page(request):
    templates_count = Connection_Spec.objects.filter(owner=request.user).__len__
    user_data = Profile.objects.get(user=request.user)

    context = {
        'templates_count': templates_count,
        'user_data': user_data,
    }
    return render(request, 'user_app/profile.html', context)

