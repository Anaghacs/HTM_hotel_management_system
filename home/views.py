from django.shortcuts import render

# Create your views here.

def index(request):
      return render(request,'commons/base.html')

def signup(request):
      return render(request,'commons/signup.html')

def logins(request):
      return render(request,'commons/logins.html')