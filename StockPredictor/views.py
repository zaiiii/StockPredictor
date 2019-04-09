from StockPredictor import settings
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.shortcuts import redirect, render

def home(request):
    return render(request, 'base.html')