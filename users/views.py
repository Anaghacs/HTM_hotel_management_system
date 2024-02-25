# from django.shortcuts import render,redirect
# from django.contrib.auth.models import User
# from django.contrib import messages,auth

# # Create your views here.

# #create login for the users.
# def users_logins(request):
#       if request.method == "POST":
#             username = request.POST['username']
#             password = request.POST['password']

#             user = auth.authenticate(username = username, password = password)

#             print("+++++++++++++============",user)

#             if user is not None:
#                   auth.login(request, user)

#                   if user.is_staff == False:
#                         return redirect('user_home')
#             else:
#                   messages.info("No such user! Please signup for the website")
#                   return redirect('user_signup')
#       return render(request,'users/users_logins.html')

# #create signup for users.
# def user_signup(request):
#       if request.method == "POST":
#             username = request.POST['username']
#             first_name = request.POST['first_name']
#             last_name = request.POST['last_name']
#             email = request.POST['email']
#             password = request.POST['password1']
#             confirm_password = request.POST['password2']

#             if password == confirm_password:
                  
#                   if User.objects.filter(username = username).exists():
#                         messages.info(request,"username is already exist! Please try some other username.")
#                         return redirect('user_signup')

#                   elif User.objects.filter(first_name = first_name).exists():
#                         messages.info(request,"firstname is already exist! Please try some other username.")
#                         return redirect('user_signup')

#                   elif User.objects.filter(last_name = last_name).exists():
#                         messages.info(request,"lastname is already exist! Please try some other username.")
#                         return redirect('user_signup')

#                   elif User.objects.filter(email = email).exists():
#                         messages.info(request,"email id is already exist! Please try some other email address.")
#                         return redirect('user_signup')
                  

#                   elif username == "" or username == " ":
#                         messages.info(request,"Username is not allowed space and blank space.")
#                         return redirect('user_signup')

#                   elif first_name == "" or first_name == " ":
#                         messages.info(request,"firstname is not allowed blank space or space.")
#                         return redirect('user_signup')

#                   elif last_name == "" or last_name == " ":
#                         messages.info(request,"lastname is not allowed space and blank space.")
#                         return redirect('user_signup')
            
#                   else:
#                         my_user = User.objects.create_user(username,email,password)
#                         my_user.first_name = first_name
#                         my_user.last_name = last_name
#                         my_user.save()
#                         return redirect('user_logins')
#             else:
#                   messages.info(request,"password and confirm password is not equal ! please verify your password.")
#                   return redirect('user_signup')
            
#             # return redirect('/')
#       return render(request,'users/signup.html')

# #login then move user-home page
# def user_home(request):
#       return render(request, 'users/users_home.html')

# #create user logout
# def user_logout(request):
#       auth.logout(request)
#       return redirect('/')

from django.urls import path
from . import views
urlpatterns = [
]

