from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages,auth
from home.models import Hotel, User, Customer, Room, Booking
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from datetime import datetime

# Create your views here.

#create signup for users.
def user_signup(request):
      if request.method == "POST":
            username = request.POST['username']
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


                  elif User.objects.filter(email = emails).exists():
                        messages.info(request,"email address is already exist! Please try some other email address.")
                        return redirect('user_signup')
                  
                  # elif User.objects.filter(phone = phone).exists():
                  #       messages.info(request,"phone number is already exist! Please try some other email address.")
                  #       return redirect('user_signup')
                  

                  elif username == "" or username == " ":
                        messages.info(request,"Username is not allowed space and blank space.")
                        return redirect('user_signup')
            
                  else:
                   
                              if role == "CUSTOMER":
                                    users=Customer.objects.create(username = username, password = password, emails = emails, phone = phone, role = role)
                                    users.save()
                                    return redirect('user_login')
            else:

                  messages.info(request,"password and confirm password is not equal ! please verify your password.")
                  return redirect('user_signup')
            
      return render(request,'users/user_signup.html')

def user_home(request):
      hotels = Hotel.objects.all()

      return render(request,'commons/indexs.html', {'hotels' : hotels})


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
      return render(request, 'commons/room-reservation.html', {'room' : room})

# def check_room_availability(request, room_number, check_in_date_str, check_out_date_str):

#       if request.method == "POST":


#       # Convert date strings to datetime objects
#             check_in = request.POST.get('check_in')
#             check_out = request.POST.get('check_out')
#             print("====================================")
#             print("===================================" ,check_in, check_out)


#       # Retrieve the room object
#             room = get_object_or_404(Room, pk = room_number)

#             overlapping_bookings = Booking.objects.filter(room = room, check_in = check_in, check_out = check_out)

#             if overlapping_bookings.exists():
#                   messages.warning(request, "not avilable ")
#             else:

#                   messages.success(request, "avilable ")
#                   # return redirect('room_booking')
#       return render(request, 'commons/room-reservation.html')

def check_room_availability(request):
    print("================================")
    if request.method == 'POST':
        # Form submitted; handle the data
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')
        # Perform any necessary processing with the form data
        # For example, you might check availability in the database

        print("===================================",check_in,check_out)
        # After processing, render a response
        return render(request, 'commons/booking.html', )
    else:
        # If it's not a POST request, render the form
        return render(request, 'commons/room-reservation.html')

# def check_room_availability(request, room_number):
#     room = get_object_or_404(Room, pk = room_number)

#     if request.method == "POST":
#         check_in = request.POST.get('check_in')
#         check_out = request.POST.get('check_out')
        
#         # Convert date strings to datetime objects
#       #   check_in = datetime.strptime(check_in_str, '%Y-%m-%dT%H:%M')
#       #   check_out = datetime.strptime(check_out_str, '%Y-%m-%dT%H:%M')

#         # Retrieve the room object
#         room = get_object_or_404(Room, pk = room_number)

#         # Check if there are any bookings overlapping with the selected dates
#         overlapping_bookings = Booking.objects.filter(room=room, chech_in=check_in, check_out=check_out)

#         if overlapping_bookings.exists():
#             messages.warning(request, "Room not available for selected dates.")
#         else:
#             messages.success(request, "Room available for booking.")
#             # You might want to redirect to a booking page here

#     # Return to the room details page after processing the form
#     return render(request, 'commons/room-reservation.html',{'room' : room})