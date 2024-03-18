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
      # Fetch the currently logged-in user
      current_user = request.user

    # Assuming the username is stored in a field called 'username'
      customer_username = current_user.username

      # return render(request,'commons/indexs.html', {'hotels' : hotels})
      return render(request, 'users/index.html', {'customer_username' : customer_username, 'hotels' : hotels})


def user_login(request):
      print("===============================")
      if request.method == "POST":
            print("===============================")
  
            username = request.POST['username']
     
            password = request.POST['password']

            customer = auth.authenticate(username = username, password = password)
            
            print("===============================", username, password)

            print("+++++++++++++============",customer)

            if customer is not None:
                  if customer.role == 'CUSTOMER':
                        auth.login(request,customer)
                        customer_id = customer.pk
                        print("=========================",customer_id)

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


   
def booking_confirmation(request):
    return render(request, 'commons/booking_confirmation.html')

def room_booking(request, room_number):
    room = get_object_or_404(Room, room_number=room_number)

    if request.method == 'POST':
        

        if request.user.is_authenticated:
            # Retrieve customer information
            try:
                if request.user.role == 'CUSTOMER':
                    customer = request.user.customer
                    print("===========================",request.user)
                else:
                    # Handle the case where the user is not a customer
                    messages.error(request, 'You need to be a customer to book a room.')
                    return redirect('user_login')
            except Customer.DoesNotExist:
                # Handle the case where the Customer object doesn't exist
                messages.error(request, 'Customer does not exist.')
                return redirect('user_login')

            room_id = room.room_number

            # Retrieve form data
            check_in = request.POST['check_in']
            check_out = request.POST['check_out']
            guest_number = request.POST['guest_number']
            print("============================",check_in,check_out,guest_number)

            # Create a new booking object
            booking = Booking.objects.create(customer=customer, room_id=room_id, check_in=check_in, check_out=check_out, guest_number=guest_number)
            booking.save()
            messages.success(request, 'Room booking successful')
            return redirect('booking_confirmation')
        else:
            messages.error(request, 'You need to log in to book a room.')
            return redirect('user_login')
    else:
        return render(request, 'commons/booking.html', {'room': room})

