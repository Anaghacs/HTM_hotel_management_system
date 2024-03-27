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
from datetime import datetime
from django.utils import timezone
from django.views.decorators.cache import never_cache

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


                  # Set session variable for authenticated hotel user
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
            # room= booking.room.room_number
            # try: 
                  
            #       counter = 1
            #       while Order.objects.filter(finder=f"{email}_{counter}").exists():
            #             counter += 1  
                  
            #       finder= f"{email}_{counter}"
            #       request.session['finder'] = finder
            #       request.session.save()
            # except Order.DoesNotExist:
            #       print("no data")
                  

            # temp=TemplateCard.objects.get(pk=temp_id)
            # currentuser=request.user.username
            # email=request.user.email
            # print(email)
            # user=User.objects.get(username=currentuser)
            
            # coupens_percentege=request.session.get('coupen_percentage',None)
            
            
                  
            # finder= request.session.get('finder',None)
            # orders=Order(customer=customer,room_id=booking.room_number,amount=booking.room.price,boock_date=timezone.now(),email_id=customer.emails,finder=finder,hotel=booking.room.hotel)
            # orders.save()
            
            # amount = booking.room.price

            # client=razorpay.Client(auth=(settings.KEY,settings.SECRET))
            # payment=client.order.create({'amount':amount * 100,'currency': 'INR','payment_capture':1})
            
            # finder= request.session.get('finder',None)
            # orders_obj=Order.objects.get(finder=finder)
            # orders_obj.razorpay_order_id=payment['id']
            # orders_obj.save()
            
            # print("*******")
            # print(payment)
            # print("*******")
            # context={
            #       "payment":payment,
            #       'booking' : booking, 
            #       'customer' : customer

      
      return render(request,'commons/booking_confirmation.html', {'booking' : booking, 'customer' :customer} )

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
            guest_number = request.POST.get('guest_number')

            # Validate check_in and check_out dates
            if not check_in or not check_out:
                messages.error(request, "Please provide both check-in and check-out dates.")
                return redirect('room_booking', room_number=room_number)

            # check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
            # check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()

            # if check_in_date < timezone.now().date():
            #     messages.error(request, "Check-in date cannot be in the past.")
            #     return redirect('room_booking', room_number=room_number)

            # if check_in_date >= check_out_date:
            #     messages.error(request, "Check-out date must be after check-in date.")
            #     return redirect('room_booking', room_number=room_number)

            overlapping_bookings = Booking.objects.filter(room=room, check_in=check_in, check_out=check_out)
            if overlapping_bookings.exists():
                messages.warning(request, "Room is not available for the selected dates.")
            
            # if guest_number >= room.capacity:
            #       messages.warning(request, "capacity is greater than guest numbers!.")
 
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

        return render(request, 'commons/booking.html', {'room' : room, 'customer' : customer})

    except Customer.DoesNotExist:
        # Handle the case where the customer does not exist
        return redirect('user_login')  # Redirect to login page or handle differently

    except Room.DoesNotExist:
        # Handle the case where the room does not exist
        messages.error(request, "The room you are trying to book does not exist.")
        return redirect('room_booking')  # Redirect to booking page or handle differently


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
                  

            # temp=TemplateCard.objects.get(pk=temp_id)
            # currentuser=request.user.username
            # email=request.user.email
            # print(email)
            # user=User.objects.get(username=currentuser)
            
            # coupens_percentege=request.session.get('coupen_percentage',None)
            
                 
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







      


