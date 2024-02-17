from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from hotels.models import Hotels

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
            return redirect('logins')
      return render(request,'commons/signup.html')

def logins(request):
      if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(username = username, password = password)

            print("+++++++++++++============",user)

            if user is not None:
                  auth_login(request, user)

                  if user.is_superuser:
                        request.session['username'] = username
                        return redirect(admin_home)
                  
                  elif user.is_staff:
                        return render(request,'users.user_home.html')
                  # else:
                  #       return render(request,'hotels.hotel_home.html')
                  
      return render(request,'commons/logins.html')

def admin_home(request):
      return render(request, 'commons/sample-page.html')

def admin_view_hotels(request):
      hotels = Hotels.objects.all()
      return render(request,'commons/admin_view_hotels.html', { 'hotels' : hotels })

def admin_view_users(request):
      users = User.objects.filter(is_superuser=False)
      return render(request,'commons/admin_view_users.html', { 'users' : users })

def approve(request,id):
      hotels = Hotels.objects.get(id = id)
      print("======================================",hotels)
      hotels.approved = True
      hotels.save()
      return redirect(admin_view_users)