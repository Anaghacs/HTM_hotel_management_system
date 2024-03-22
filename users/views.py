from time import timezone
from django.conf import settings
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages,auth
from home.models import Hotel, Order, User, Customer, Room, Booking
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from datetime import datetime
from django.utils import timezone

import razorpay
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
            # all done payment avunudo acc active avanam ath egane activate akum ???jus wait
      # user loin cheyy ok ennitt pay cheyyunna avide poo bakki njan okkaa ok
            # admin dashboard lek pokunu y ni user id and pass taa username : admin pswd : admin

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

def booking_confirmation(request):

      if 'customer_id' in request.session:
            customer_id = request.session['customer_id']
            # hotel = Hotel.objects.get(id = hotel_id)
            customer = get_object_or_404(Customer, id = customer_id)


            print("================================",customer.username)
            booking = Booking.objects.filter( customer = customer)
            print("==========================================",booking)
            # email=customer.emails
            # room= booking.room.room_number
            # print("===========================",email,room)
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
            
            
            # ith anu function ok no raksha
                  
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

            # }
      
      return render(request,'commons/booking_confirmation.html', {'booking' : booking, 'customer' :customer} )

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
      


# def checkout(request,temp_id):
#     if not request.user.is_authenticated:
#         messages.warning(request,"Login & Try Again")
#         return redirect('register:login')
#     if request.method=="POST":
#         email=request.user.email
#         try: 
            
#             counter = 1
#             while Orders.objects.filter(finder=f"{email}_{counter}").exists():
#                 counter += 1  
            
#             finder= f"{email}_{counter}"
#             request.session['finder'] = finder
#             request.session.save()
#         except Orders.DoesNotExist:
#             print("no data")
              

#         temp=TemplateCard.objects.get(pk=temp_id)
#         currentuser=request.user.username
#         email=request.user.email
#         print(email)
#         user=User.objects.get(username=currentuser)
        
#         # coupens_percentege=request.session.get('coupen_percentage',None)
        
#         if request.session.get('final_price',None):
#             final_amount=request.session.get('final_price',None)
#             print(final_amount)
#             print(temp.price)
#         else:
#             final_amount=int(temp.price)
#             print(type(final_amount))

             
#         finder= request.session.get('finder',None)
#         code = request.session.get('coupen_code',None)
#         number=request.POST.get('number','')
#         orders=Orders(name=user.first_name,temp_name=temp.model_name,temp_amount=temp.price,ordered_date=timezone.now(),email_id=email,finder=finder,phone=number,final_amount=final_amount,coupen_code=code)
#         orders.save()

#     client=razorpay.Client(auth=(settings.KEY,settings.SECRET))
#     payment=client.order.create({'amount':final_amount * 100,'currency': 'INR','payment_capture':1})
#     finder= request.session.get('finder',None)
#     orders_obj=Orders.objects.get(finder=finder)
#     orders_obj.razorpay_order_id=payment['id']
#     orders_obj.save()
#     print("*******")
#     print(payment)
#     print("*******")
#     context={
#         "payment":payment

#     }
#     if 'code' in request.session:
#         del request.session['code']
#         del request.session['percentage']
#         del request.session['final_price']
#         request.session.save()
#         print("deleted")

#     return render(request,"checkout.html",context)
# booking id vende ss aaa a booking id get cheyth eduthal room id customer id kitile booking i undo in build ayit create cheyomo oru id get cheytha edutha mathi but model il booking id store cheyan ou filed vende wait
# def paymentfaild(request):
#     if not request.user.is_authenticated:
#         messages.warning(request,"Login & Try Again")
#         return redirect('register:login')
#     order_id=request.GET.get('Order_id')
#     orders=Orders.objects.get(razorpay_order_id=order_id)
#     orders.amountpaid= False
#     orders.paymentstatus = "failed"
#     print("faild")
#     orders.save()

#     orders_id=request.GET.get('Order_id')
#     print(orders_id)
#     reason=request.GET.get('reason')
#     code=request.GET.get('code')
#     source=request.GET.get('source')
#     step=request.GET.get('step')
#     payment_id=request.GET.get('payment_id')
#     if PaymentFailed.objects.filter(order_id=orders_id).exists():
        
#         print("failed alredy exists")
#         return redirect('tedsilapp:somethingwentwrong')
#     else:
#         try:
#             failed=PaymentFailed(order_id=orders_id,reason=reason,code=code,source=source,step=step,payment_id=payment_id,date_time=timezone.now())
#             failed.save()
#             time=timezone.now()
#             uid=request.user.id
#             uemail=request.user.email
#             uname=request.user.first_name
#             email_subject="payment failed"
#             message=render_to_string('payment_failure_mail.html',{
#                 'orders_id':orders_id,
#                 'reason':reason,
#                 'code':code,
#                 'source':source,
#                 'step':step,
#                 'payment_id':payment_id,
#                 'uid':uid,
#                 'uname':uname,
#                 'uemail':uemail,
#                 'date':time

#             })
#             print("mail attemptting")
#             email_from = settings.EMAIL_HOST_USER
#             recipient_list = ['attackerhacker507@gmail.com']

#             email_message = EmailMessage(email_subject,message,email_from,recipient_list)
#             print(email_message)
#             email_message.content_subtype = "html"
#             email_message.send()
#             if 'code' in request.session:
#                 del request.session['code']
#                 del request.session['percentage']
#                 del request.session['final_price']
#                 request.session.save()
#                 print("deleted")
            

            
#         except  Exception as e:
            
#             print("something went wrong")
#             print(f"Error sending email: {e}")
#             return redirect('tedsilapp:somethingwentwrong')
#     return render(request,"paymentfaild.html",{'order_id': order_id})

def paymentsuccess(request):
#     if not request.user.is_authenticated:
#         messages.warning(request,"Login & Try Again")
#         return redirect('register:login')
    
    order_id=request.GET.get('Order_id')
    customer_id = request.session['customer_id']
    customer = Customer.objects.get(id=customer_id)
    orders=Order.objects.get(razorpay_order_id=order_id)
    print(orders)
    orders.paid_amount= True
    orders.status = "paid"
    orders.save()
#     try:
        # time=timezone.now()
        
      #   order_success=Order.objects.get(razorpay_order_id=order_id)
        
      #   uid=request.user.id
      #   uemail=request.user.email
      #   uname=request.user.first_name
      #   coupen_code=order_success.coupen_code
      #   razorpay_payment_id=order_success.razorpay_payment_id
      #   temp_name=order_success.temp_name
      #   temp_amount=order_success.temp_amount
      #   plan=order_success.plan
      #   final_amount=order_success.final_amount
      #   ordered_date=order_success.ordered_date

        # renewal
        # uusernam=request.user.username
        # date=order_success.ordered_date


        # renewals= Renewal.objects

      #   email_subject="Order Placed"
      #   message=render_to_string('payment_sucess_mail.html',{
      #       'orders_id':order_id,
      #       'uname':uname,
      #       'uemail':uemail,
      #       'coupen_code':coupen_code,
      #       'razorpay_payment_id':razorpay_payment_id,
      #       'temp_name':temp_name,
      #       'temp_amount':temp_amount,
      #       'plan':plan,
      #       'final_amount':final_amount,
      #       'uid':uid,
      #       'date':ordered_date

      #   })
      #   print("mail attemptting")
      #   email_from = settings.EMAIL_HOST_USER
      #   recipient_list = ['attackerhacker507@gmail.com']

      #   email_message = EmailMessage(email_subject,message,email_from,recipient_list)
      #   print(email_message)
      #   email_message.content_subtype = "html"
      #   email_message.send()


        # mail for users
        
      #   email_subject="your order has placed"
      #   message=render_to_string('payment_sucess_user_mail.html',{
      #       'orders_id':str(order_id),
      #       'uname':uname,
      #       'uemail':uemail,
      #       'coupen_code':coupen_code,
      #       'razorpay_payment_id':razorpay_payment_id,
      #       'temp_name':temp_name,
      #       'temp_amount':temp_amount,
      #       'plan':plan,
      #       'final_amount':final_amount,
      #       'uid':uid,
      #       'date':ordered_date

      #   })
      #   print("mail attemptting")
      #   email_from = settings.EMAIL_HOST_USER
      #   recipient_list = [uemail]

      #   email_message = EmailMessage(email_subject,message,email_from,recipient_list)
      #   print(email_message)
      #   email_message.content_subtype = "html"
      #   email_message.send()

        
            

            
#     except  Exception as e:
            
#             print("something went wrong")
#             print(f"Error sending email: {e}")
#             return redirect('tedsilapp:somethingwentwrong')
    return render(request,"users/paymentsuccess.html") 