from django.shortcuts import render,redirect
from django.contrib.auth.models import User

# Create your views here.

def index(request):
      return render(request,'commons/index.html')

def signup(request):
      if request.method == "POST":
            username = request.POST['username']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            password = request.POST['password1']
            confirm_password = request.POST['password2']

            my_user = User.objects.create_user(username,email,password)
            my_user.first_name = first_name
            my_user.last_name = last_name
            my_user.save()
            return redirect('login')
      return render(request,'commons/signup.html')

def logins(request):
      
      return render(request,'commons/logins.html')