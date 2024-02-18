from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages,auth

# Create your views here.

#create user signup
def signup(request):
      if request.method == "POST":
            username = request.POST['username']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            password = request.POST['password1']
            confirm_password = request.POST['password2']

            if username == "" or username == " ":
                  messages.info(request,"Username is not allowed space and blank space.")
                  return redirect('signup')

            elif first_name == "" or first_name == " ":
                  messages.info(request,"firstname is not allowed blank space or space.")
                  return redirect('signup')

            if last_name == "" or last_name == " ":
                  messages.info(request,"lastname is not allowed space and blank space.")
                  return redirect('signup')

            elif User.objects.filter(username = username).exists():
                  messages.info(request,"username is already exist! Please try some other username.")
                  return redirect('signup')

            elif User.objects.filter(email = email).exists():
                  messages.info(request,"email id is already exist! Please try some other email address.")
                  return redirect('signup')
            
            elif password != confirm_password:
                  messages.info(request,"password and confirm password is not equal ! please verify your password.")
                  return redirect('signup')
            else:
                  my_user = User.objects.create_user(username,email,password)
                  my_user.first_name = first_name
                  my_user.last_name = last_name
                  my_user.save()
                  return redirect('logins')
      return render(request,'users/signup.html')

def user_home(request):
      return render(request, 'users/users_home.html')

