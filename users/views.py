from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages,auth
from home.models import Hotel, User, Customer, Room
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

# Create your views here.

#create signup for users.
def user_signup(request):
      if request.method == "POST":
            username = request.POST['username']
            # first_name = request.POST['first_name']
            # last_name = request.POST['last_name']
            # address = request.POST['address']
            # place = request.POST['place']
            emails = request.POST['email']
            password = request.POST['password1']
            confirm_password = request.POST['password2']
            phone = request.POST['phone']
            role = request.POST['role']

            if password == confirm_password:
                  
                  if User.objects.filter(username = username).exists():
                        messages.info(request,"username is already exist! Please try some other username.")
                        return redirect('user_signup')

                  # elif User.objects.filter(first_name = first_name).exists():
                  #       messages.info(request,"firstname is already exist! Please try some other username.")
                  #       return redirect('user_signup')

                  # elif User.objects.filter(last_name = last_name).exists():
                  #       messages.info(request,"lastname is already exist! Please try some other username.")
                  #       return redirect('user_signup')

                  elif User.objects.filter(email = emails).exists():
                        messages.info(request,"email address is already exist! Please try some other email address.")
                        return redirect('user_signup')
                  
                  # elif User.objects.filter(phone = phone).exists():
                  #       messages.info(request,"phone number is already exist! Please try some other email address.")
                  #       return redirect('user_signup')
                  

                  elif username == "" or username == " ":
                        messages.info(request,"Username is not allowed space and blank space.")
                        return redirect('user_signup')

                  # elif first_name == "" or first_name == " ":
                  #       messages.info(request,"firstname is not allowed blank space or space.")
                  #       return redirect('user_signup')

                  # elif last_name == "" or last_name == " ":
                  #       messages.info(request,"lastname is not allowed space and blank space.")
                  #       return redirect('user_signup')
            
                  else:
                   
                        # try:
                              if role == "CUSTOMER":
                                    users=Customer.objects.create(username = username, password = password, emails = emails, phone = phone, role = role)
                                    users.save()
                                    return redirect('user_login')
                        # except:
            else:

                  messages.info(request,"password and confirm password is not equal ! please verify your password.")
                  return redirect('user_signup')
            
            # return redirect('/')
      return render(request,'users/user_signup.html')

def user_home(request):
      hotels = Hotel.objects.all()

      return render(request,'commons/indexs.html', {'hotels' : hotels})

# #login then move user-home page
# def user_home(request):
#       return render(request,'users/indexs.html')

# #create user logout
# def user_logout(request):
#       auth.logout(request)
#       return redirect('/')



def user_login(request):
      print("===============================")
      if request.method == "POST":
            print("===============================")
  
            username = request.POST['username']
            password = request.POST['password']

            customer = auth.authenticate(username = username, password = password)
            
            print("===============================", username, password)
            # customer =Customer.objects.get(username = username, password = password)
            print("+++++++++++++============",customer)

            if customer is not None:
                  if customer.role == 'CUSTOMER':
                        auth.login(request,customer)
                        return redirect(user_home)        
            else:
                  messages.info(request,"Username and password is not registered! Please signup first.")  
      return render(request,'users/user_login.html')


@login_required
def user_logout(request):
      logout(request)
      return redirect('index')

def room_list(request, id):
      hotel = get_object_or_404(Hotel, id = id)

      rooms = Room.objects.filter(is_deleted = False, hotel = hotel)
      return render(request, 'commons/room-list.html', {'hotel' : hotel,'rooms' : rooms})

def room_reservation(request, room_number):

      room = get_object_or_404(Room, room_number = room_number)
      

      # rooms = Room.objects.filter(is_deleted = False, hotel = hotel)
      return render(request, 'commons/room-reservation.html', {'room' : room})