from StockPredictor import settings
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.views import generic
from .forms import RegistrationForm


@login_required()
def home(request):
    return render(request, 'base.html')

def loginview(request):
    global user
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(request, 'base.html')
            else:
                return render(request, 'registration/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'registration/login.html', {'error_message': 'Invalid login'})
    return redirect(request, 'base.html')

# def logoutview(request):
#     logout(request)
#     return redirect(request, 'login')

def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            print(username, raw_password)
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(request, 'base.html')
        else :
            print(form.errors)
            # return render('signup.html', {'form': form})

    else:
        form = RegistrationForm()
    return render(request, 'registration/signup.html', {'form': form})


# class SignUp(generic.CreateView):
#     form_class = RegistrationForm
#     success_url = reverse_lazy('login')
#     template_name = 'registration/signup.html'
#     return redirect(request, 'base.html')