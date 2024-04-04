from time import timezone
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages,auth
from home.models import Hotel, Order, User, Customer, Room, Booking
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
from django.utils import timezone
from django.views.decorators.cache import never_cache
from users.models import Storedotps

from django.http import JsonResponse
from django.core.mail import send_mail
import random

import razorpay

import os

GTK_FOLDER=r"C:\Program Files\GTK3-Runtime Win64\bin"
os.environ['PATH'] = GTK_FOLDER


from django.template.loader import render_to_string
from weasyprint import HTML

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

@never_cache
def user_login(request):
      print("=================================")
      if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            print("===============================", username, password)


            try:
                  customer = Customer.objects.get(username = username, password = password)
                  print("===============================", customer)


                  # Set session variable for authenticated hotel user userine login enganeyaa cheyykkunne customer num hotel nem same thaneya athupole thazhe cheyy nth login
                  request.session['customer_id'] = customer.id
                  return redirect('user_home')
            except Hotel.DoesNotExist:
                  messages.error(request, "Invalid credentials or account not approved.")
    
      return render(request, 'users/user_login.html')

#customer logout
@never_cache
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
      return render(request, 'commons/room-reservation.html', {'room' : room, })



from django.db.models import Q
from datetime import datetime
#customer check_availability
# def check_room_availability(request, room_number):
#       print("================================")
#       room = get_object_or_404(Room, room_number = room_number)
    
#       # if 'customer_id' in request.session:
#       #       customer_id = request.session['customer_id']
#       #       customer = get_object_or_404(Customer, id=customer_id)
#       #       print("==========================", customer)

#       if request.method == 'POST':
#             check_in = request.POST.get('check_in')
#             check_out = request.POST.get('check_out')

#             print("===================================", check_in, check_out, room)
            

# # Assuming room, check_in, and check_out are provided
#             overlapping_bookings = Booking.objects.filter(
#             Q(room=room) &
#             (
#                   Q(check_in__lte=check_in, check_out__gte=check_in) |  # Booking starts before new check-in
#                   Q(check_in__lte=check_out, check_out__gte=check_out) |  # Booking ends after new check-out
#                   Q(check_in__gte=check_in, check_out__lte=check_out)  # Booking starts and ends within new booking dates
#             )
#             )

# # This will give you all bookings that overlap with the provided check-in and check-out dates for the specified room.

#             # overlapping_bookings = Booking.objects.filter(room = room, check_in = check_in, check_out = check_out)
        
#             if overlapping_bookings.exists():
#                   messages.warning(request, "Room is not available! Please change date.")

#             else:
#                   # After processing, render a response one minit waitok
#                   messages.success(request, "Room is available")

#                   return render(request, 'commons/room-reservation.html')
    
#       # If it's not a POST request or there's an overlapping booking, render the form
#       return render(request, 'commons/room-reservation.html', {'room': room, })



def check_room_availability(request, room_number):
    room = get_object_or_404(Room, room_number=room_number)

    if request.method == 'POST':
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')

        overlapping_bookings = Booking.objects.filter(
            Q(room=room) &
            (
                Q(check_in__lte=check_in, check_out__gte=check_in) |  # Booking starts before new check-in
                Q(check_in__lte=check_out, check_out__gte=check_out) |  # Booking ends after new check-out
                Q(check_in__gte=check_in, check_out__lte=check_out)  # Booking starts and ends within new booking dates
            )
        )
# booking cheyona baghath kudi nerathe cheytha pole check cheyanam and person number kudi check cheyth true anukile booking cheyan padulu views 
        if overlapping_bookings.exists():
            messages.warning(request, "Room is not available! Please change date.")
        else:
            messages.success(request, "Room is available")
            return render(request, 'commons/room-reservation.html')

    # If it's not a POST request or there's an overlapping booking, render the form
    return render(request, 'commons/room-reservation.html', {'room': room})

@never_cache
def booking_confirmation(request):

      if 'customer_id' in request.session:
            customer_id = request.session['customer_id']
            # hotel = Hotel.objects.get(id = hotel_id)
            customer = get_object_or_404(Customer, id = customer_id)


            print("================================",customer.username)
            booking = Booking.objects.filter( customer = customer)
            print("==========================================",booking)
            email=customer.emails
            order = Order.objects.filter(customer=customer)
            # print(order.id)
            for i in order:
                 print(i.paid_amount,"order")

            
                 

      return render(request,'commons/booking_confirmation.html', {'booking' : booking, 'customer' :customer, 'order' : order} )

# @never_cache
# def room_booking(request, room_number):
# #     evide kudi check cheythit venam booking cheyan capacity and form le guest number check cheythit less or equal anukil mathrem book cheyabam
#     try:
#         customer_id = request.session.get('customer_id')
#         if not customer_id:
#             return redirect('user_login')  # Redirect to login page if user is not logged in

#         customer = Customer.objects.get(id=customer_id)
#         room = Room.objects.get(room_number=room_number)

#         if request.method == "POST":
#             check_in = request.POST.get('check_in')
#             check_out = request.POST.get('check_out')
#             guest_number = request.POST.get('guest_number')

#             # Validate check_in and check_out dates
#             if not check_in or not check_out:
#                 messages.error(request, "Please provide both check-in and check-out dates.")
#                 return redirect('room_booking', room_number=room_number)

#             # check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
#             # check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()

#             # if check_in_date < timezone.now().date():
#             #     messages.error(request, "Check-in date cannot be in the past.")
#             #     return redirect('room_booking', room_number=room_number)

#             # if check_in_date >= check_out_date:
#             #     messages.error(request, "Check-out date must be after check-in date.")
#             #     return redirect('room_booking', room_number=room_number)

#             overlapping_bookings = Booking.objects.filter(room=room, check_in=check_in, check_out=check_out)
#             if overlapping_bookings.exists():
#                 messages.warning(request, "Room is not available for the selected dates.")
            
#             # if guest_number >= room.capacity:
#             #       messages.warning(request, "capacity is greater than guest numbers!.")
 
#             else:
#                 booking = Booking.objects.create(
#                     customer=customer,
#                     check_in=check_in,
#                     check_out=check_out,
#                     guest_number=guest_number,
#                     room=room,
#                 )
#                 booking.save()
#                 messages.success(request, "Room is available and booking is successful.")
#                 return redirect('booking_confirmation')

#         return render(request, 'commons/booking.html', {'room' : room, 'customer' : customer})

#     except Customer.DoesNotExist:
#         # Handle the case where the customer does not exist
#         return redirect('user_login')  # Redirect to login page or handle differently

#     except Room.DoesNotExist:
#         # Handle the case where the room does not exist
#         messages.error(request, "The room you are trying to book does not exist.")
#         return redirect('room_booking')  # Redirect to booking page or handle differently












@never_cache
def room_booking(request, room_number):
    try:
        customer_id = request.session.get('customer_id')
        if not customer_id:
            return redirect('user_login')  # Redirect to login page if user is not logged in

        customer = Customer.objects.get(id=customer_id)
        room = Room.objects.get(room_number=room_number)

        if request.method == "POST":
            check_in = request.POST.get('check_in')
            check_out = request.POST.get('check_out')
            guest_number = int(request.POST.get('guest_number'))

            # Validate check_in and check_out dates
            if not check_in or not check_out:
                messages.error(request, "Please provide both check-in and check-out dates.")
                return redirect('room_booking', room_number=room_number)

            check_in_date = datetime.strptime(check_in, '%Y-%m-%dT%H:%M').date()
            check_out_date = datetime.strptime(check_out, '%Y-%m-%dT%H:%M').date()

            if check_in_date < datetime.now().date():
                messages.error(request, "Check-in date cannot be in the past.")
                return redirect('room_booking', room_number=room_number)

            if check_in_date >= check_out_date:
                messages.error(request, "Check-out date must be after check-in date.")
                return redirect('room_booking', room_number=room_number)
# but room booking anu en kanikunilalo wait onu nokte error und bcz ee date already booking cheythit und ee room manasilayilla
            # Check if there are any bookings for the specified room and dates
            existing_checkin = Booking.objects.filter(
                  room=room,
                  check_in__lte=check_out_date,  # Check if the existing booking's check-in date is before or on the new check-out date
                  check_out__gt=check_in_date  # Check if the existing booking's check-out date is strictly after the new check-in date
            )

            existing_checkout = Booking.objects.filter(
                  room=room,
                  check_in__lt=check_out_date,  # Check if the existing booking's check-in date is strictly before the new check-out date
                  check_out__gte=check_in_date  # Check if the existing booking's check-out date is after or on the new check-in date
            )

            existing_overlap = existing_checkin.exists() or existing_checkout.exists()

            if existing_overlap:
                  messages.warning(request, "Room is not available for the selected dates.")
                  return redirect('room_booking', room_number=room_number)
            
            
            # Check if the number of guests exceeds the room capacity
            if guest_number > room.capacity:
                messages.error(request, f"Guest number exceeds the room capacity ({room.capacity}).")
                return redirect('room_booking', room_number=room_number)

            # overlapping_bookings = Booking.objects.filter(room=room, check_in=check_in, check_out=check_out)
            # if overlapping_bookings.exists():
            #     messages.warning(request, "Room is not available for the selected dates.")
            else:
                booking = Booking.objects.create(
                    customer=customer,
                    check_in=check_in,
                    check_out=check_out,
                    guest_number=guest_number,
                    room=room,
                )
                booking.save()
                messages.success(request, "Room is available and booking is successful.")
                return redirect('booking_confirmation')

        return render(request, 'commons/booking.html', {'room': room, 'customer': customer})

    except Customer.DoesNotExist:
        # Handle the case where the customer does not exist
        return redirect('user_login')  # Redirect to login page or handle differently
#     check cheyy ok set ini und already paid cheythit ula room te confirmation mathit oru p tag il already paid en kanikanam pine amount calculation views

    except Room.DoesNotExist:
        # Handle the case where the room does not exist
        messages.error(request, "The room you are trying to book does not exist.")
        return redirect('room_booking')  # Redirect to booking page or handle differently


#  check cheyy error poyaaaa????























# #customer booking_confirmation 
@never_cache 
def confirmation(request, id):
    booking = get_object_or_404(Booking, id = id)
    if 'customer_id' in request.session:
            customer_id = request.session['customer_id']
            # hotel = Hotel.objects.get(id = hotel_id)
            customer = get_object_or_404(Customer, id = customer_id)


            print("================================",customer.username)
            print("==========================================",booking)

            # ippoll antha cheyyende ee page kandile athil confirmation il butto ale kanikune?? but oru vattam payment cheythit ula rooms ind ithil athil payment nadathit undakil p tag il payment completed en kanikanam payment nadathathathil cinfirmation button nu pakaram payment button il dy calculate cheytha amount kanikanam ee page venda pakaram ee page il payment te button varanam
            # models edukk aa html eduk

            email=customer.emails
            # room= booking.room.room_number
            print("===========================",email)
            try: 
                  
                  counter = 1
                  while Order.objects.filter(finder=f"{email}_{counter}").exists():
                        counter += 1  
                  
                  finder= f"{email}_{counter}"
                  request.session['finder'] = finder
                  request.session.save()
            except Order.DoesNotExist:
                  print("no data")
                  
                 
            finder= request.session.get('finder',None)
            orders=Order(customer=customer,room_id=booking.room.room_number,amount=booking.room.price,boock_date=timezone.now(),email_id=booking.customer.emails,finder=finder,hotel=booking.room.hotel)
            orders.save()
            
            amounts = booking.room.price
            print(type(amounts))
            print(amounts)
            amount=int(amounts)

            print(amount) 
            print(type(amount))

            client=razorpay.Client(auth=(settings.KEY,settings.SECRET))
            payment=client.order.create({'amount':amount * 100,'currency': 'INR','payment_capture':1})
            
            finder= request.session.get('finder',None)
            orders_obj=Order.objects.get(finder=finder)
            orders_obj.razorpay_order_id=payment['id']
            orders_obj.save() 
            
            print("*******")
            print(payment)
            print("*******")
            context={
                  'payment' :payment,
                  'booking' : booking, 
                  'customer' : customer,
                  'amount' : amount

            }
    return render(request, 'users/booking_confirmation.html', context )


@login_required
@never_cache
def paymentsuccess(request):
    
#     if not request.user.is_authenticated:
#         messages.warning(request,"Login & Try Again")
#         return redirect('register:login')
    
    
    order_id=request.GET.get('Order_id')
    print(type(order_id))
    customer_id = request.session['customer_id']
    customer = Customer.objects.get(id=customer_id)
    orders=Order.objects.get(razorpay_order_id=order_id)
    
    print(orders)
    orders.paid_amount= True
    orders.status = "paid"
    orders.save()
    return render(request,"users/paymentsuccess.html", {'orders' : orders, 'customer' : customer}) 

@never_cache
def booking_details_pdf(request):

      try:
            order_id=request.GET.get('Order_id')

            if Order.objects.filter(razorpay_order_id=order_id).exists():
                  order =Order.objects.get(razorpay_order_id=order_id)

                  # Render HTML template with data
                  html_string = render_to_string('users/booking_pdf.html', {'order': order})

                  # Create PDF from HTML string
                  # pdf_file = HTML(string=html_string).write_pdf()
                  html = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()

                   # Set response type as PDF
            response = HttpResponse(html, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="booking_confirmation.pdf"'

            return response
      except Order.DoesNotExist:
            print("Order not found in table")
      return render(request,"users/booking_pdf.html")


def generate_and_send_otp(request):
      print("==============================hiiiiiiiii")
      if request.method == 'POST':
            email = request.POST.get('email')
            request.session['user_email'] = email
            print("============================", email)
            request.session.save()
            user_email=request.session.get('user_email',None)
            print("==============================", user_email)
            if email:
                  if Customer.objects.filter(email=email).exists():
                        OTP = random.randint(100000, 999999)
                        print(OTP)    
                        print("otp",OTP)
                        user = Customer.objects.get(email=email)
                        print("===================")
                        subject = 'OTP Verification'
                        message = f'Hi {user.username},Your Forgott Password OTP is  {OTP}  Valid For 5 Minit. Do Not Share. if you not requested for otp then ignore it'
                        email_from = settings.EMAIL_HOST_USER
                        recipient_list = {email}

                        send_mail( subject, 
                              message, 
                              email_from, 
                              recipient_list )
                        messages.info(request, f"We will send an OTP to the email '{email}'")
                        
                        if Storedotps.objects.filter(email_id=request.session.get('user_email', None)).exists():
                              Storedotps.objects.filter(email_id=request.session.get('user_email', None)).update(otp=OTP,valid_from=timezone.now(),is_active=True)
                
                        else:
                              otp_data=Storedotps.objects.create(email_id=user.email,otp=OTP,valid_from=timezone.now())
                              otp_data.save()
                        # request.session['otp'] = OTP  # Store OTP in session for verification
                        return JsonResponse({'success': True})                  
                  else:
                        messages.error(request,"Email is not registered on our site.")
                        return redirect('user_login')
            else:
                  return JsonResponse({'success': False, 'error': 'Email not provided'})
      else:       
            return JsonResponse({'success': False, 'error': 'Only POST requests are allowed'})
      
      

# otp experation
def is_otp_expired(otp_data):
    expiration_duration = timedelta(minutes=5)  
    now = timezone.now()
    print("expire checking...")
    return now - otp_data.valid_from > expiration_duration


# 
def validate_otp (request):
    if request.method == 'POST':
        otp_valid=request.POST['otp']
        user_email = request.session.get('user_email', None)
        print(user_email)
        
        
        try:
            otp_data = Storedotps.objects.get(email_id=user_email, is_active=True)
        except Storedotps.DoesNotExist:
            messages.error(request, "Invalid OTP or OTP has expired.")
            return redirect('user_login')
        
        if otp_valid == str(otp_data.otp):
            if not is_otp_expired(otp_data):
                otp_data.is_active = False 
                print("otp valid") 
                otp_data.save()
                user=Customer.objects.get(email=user_email)
                print(user)
                request.session['customer_id'] = user.id
                return redirect('user_home')
            
            else:
                messages.error(request, "otp is expired")
                otp_data.is_active = False
                print("otp is expired")
                return redirect('user_login')  
            
        else:
            messages.error(request, "Invalid OTP or OTP has expired.")
            
            return redirect('user_login')
    return render(request, "users/forgott_password.html")


def forgot_password(request):
      return render(request,"users/forgott_password.html")


def room_reservation_details(request):
      order=request.GET.get('Order_id')

      if 'customer_id' in request.session:
            customer_id = request.session['customer_id']
            # hotel = Hotel.objects.get(id = hotel_id)
            customer = get_object_or_404(Customer, id = customer_id)
            booking = Booking.objects.filter(customer = customer)
            orders = Order.objects.filter(customer = customer)


            print("================================",customer.username)
      return render(request, 'users/page-account-register.html',{'orders' : orders,'customer' : customer, 'booking' : booking})