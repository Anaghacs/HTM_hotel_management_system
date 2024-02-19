from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from hotels.models import Hotels
from django.contrib.auth import logout
from users.views import user_home

# Create your views here.

def index(request):
      return render(request,'commons/index.html')

#login functions
def logins(request):
      if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(username = username, password = password)

            print("+++++++++++++============",user.__dict__)

            if user is not None:
                  auth_login(request, user)

                  if user.is_superuser:
                        request.session['username'] = username
                        return redirect(admin_home)
                  
                  elif user:
                        return redirect(user_home)
                  
                  elif user.approved == True:
                        return render(request,'hotels.hotel_home.html')
                  
      return render(request,'commons/logins.html')

def admin_home(request):
      return render(request, 'commons/sample-page.html')

def admin_view_hotels(request):
      hotels = Hotels.objects.all()
      return render(request,'commons/admin_view_hotels.html', {'hotels':hotels})

def admin_view_users(request):
      users = User.objects.filter(is_superuser=False)
      return render(request,'commons/admin_view_users.html', { 'users' : users })

def approve(request,id):
      hotels = Hotels.objects.get(id = id)
      print("======================================",hotels)
      hotels.approved = True
      hotels.save()
      return redirect(admin_view_users)

def signout(request):
    logout(request)
    return redirect('index')