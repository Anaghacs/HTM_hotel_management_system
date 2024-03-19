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
      if 'customer_id' in request.session:
            customer_id = request.session['customer_id']
            try:
                  customer_username = Customer.objects.get(id = customer_id)
                  hotels = Hotel.objects.all()

                  # customers = Customer.objects.all()
                  return render(request, 'users/index.html', {'customer_username': customer_username, 'hotels' : hotels})
            
            
            except customer_username.DoesNotExist:
                  # Handle case where hotel with given ID does not exist
                  del request.session['customer_id']
    
      # Redirect to login page if user is not authenticated
      return redirect('user_login')


def user_login(request):
      print("=================================")
      if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            print("===============================", username, password)


            try:
                  customer = Customer.objects.get(username = username, password = password)
                  print("===============================", customer)


                  # Set session variable for authenticated hotel user
                  request.session['customer_id'] = customer.id
                  return redirect('user_home')
      
            except Hotel.DoesNotExist:
                  messages.error(request, "Invalid credentials or account not approved.")
    
      return render(request, 'users/user_login.html')

#customer logout
def user_logout(request):
    # Clear the session data
    request.session.flush()
    # Redirect to the login page or any other desired page
    return redirect('index')

#customer room list
def room_list(request, id):
      hotel = get_object_or_404(Hotel, id = id)
      rooms = Room.objects.filter(is_deleted = False, hotel = hotel)
      return render(request, 'commons/room-list.html', {'hotel' : hotel,'rooms' : rooms})

#customer room reservation
def room_reservation(request, room_number):
      room = get_object_or_404(Room, room_number = room_number)
      return render(request, 'commons/room-reservation.html', {'room' : room})

#customer check_availability
def check_room_availability(request, room_number):
      print("================================")
      room = get_object_or_404(Room, room_number = room_number)

      if request.method == 'POST':
            # Form submitted; handle the data
            check_in = request.POST.get('check_in')
            check_out = request.POST.get('check_out')

            print("===================================", check_in, check_out, room)
            overlapping_bookings = Booking.objects.filter(room = room, check_in = check_in, check_out = check_out)
        
            if overlapping_bookings.exists():
                  messages.warning(request, "Room is not available! Please change date.")

            else:
                  # After processing, render a response
                  messages.success(request, "Room is available")

                  return render(request, 'commons/room-reservation.html')
    
      # If it's not a POST request or there's an overlapping booking, render the form
      return render(request, 'commons/room-reservation.html', {'room': room})

# #customer booking_confirmation  
# def booking_confirmation(request):
# #     booking = get_object_or_404(Booking, )
#     return render(request, 'commons/booking_confirmation.html')

def booking_confirmation(request):

      if 'customer_id' in request.session:
            customer_id = request.session['customer_id']
            # hotel = Hotel.objects.get(id = hotel_id)
            customer = get_object_or_404(Customer, id = customer_id)


            print("================================",customer.username)
            booking = Booking.objects.filter( customer = customer)
            print("==========================================",booking)
      return render(request,'commons/booking_confirmation.html', {'booking' : booking, 'customer' : customer})

def room_booking(request, room_number):
      try:
            customer_id = request.session['customer_id']
            customer = Customer.objects.get(id=customer_id)
            room = Room.objects.get(room_number=room_number)

            if request.method == "POST":
                  check_in = request.POST['check_in']
                  check_out = request.POST['check_out']
                  guest_number = request.POST['guest_number']
                  
                  booking = Booking.objects.create(
                  customer=customer,
                  check_in=check_in,
                  check_out=check_out,
                  guest_number=guest_number,
                  room=room,
                  )
                  booking.save()
                  messages.success(request, "Your booking record has been successfully added!")
                  return redirect('booking_confirmation')

            return render(request, 'commons/booking.html', {'room': room,})

      except KeyError:
        # If 'customer_id' is not found in session, user is not logged in
        # Redirect to login page or handle the situation accordingly
            return redirect('user_login')
      except Customer.DoesNotExist:
        # Handle the case where the customer does not exist
        # This could happen if the session contains an invalid customer_id
            return redirect('user_login')  # Redirect to login page or handle differently
      except Room.DoesNotExist:
        # Handle the case where the room does not exist
        # This could happen if the room_number provided is invalid
        messages.error(request, "The room you are trying to book does not exist.")
        return redirect('room_booking')  # Redirect to booking page or handle differently
      