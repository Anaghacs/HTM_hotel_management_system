from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from home.models import Hotel, User, Customer, Room
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


def hotel_signup(request):
      error = ""
      if request.method == "POST":
            
            hotel_name = request.POST['hotel_name']
            username = request.POST['username']
            password = request.POST['password']
            address = request.POST['address']
            place = request.POST['place']
            emails = request.POST['emails']
            phone = request.POST['phone']

            #photo file get
            photo = request.FILES.get('photo')
            role = request.POST['role']
            print("==================================",hotel_name, emails, username, password)

            
            if hotel_name == "" or hotel_name == " ":
                  messages.info(request,"hotelname is not allowed space and blank space and not allowed special characters")
                  return redirect(hotel_signup)
            
            elif address == "" or address == "":
                  messages.info(request,"address is not allowed space and blank space and not allowed special characte")
                  return redirect(hotel_signup)
            
            
            elif place == "" or place == "":
                  messages.info(request,"place is not allowed space and blank space and special character")
                  return redirect(hotel_signup)
            
            else:
                  try:
                  #create hotel model and insert the data
                        if role == "HOTEL":
                              # hotels = Hotel.objects.create(hotel_name = hotel_name, address = address, place = place, phone = phone, emails = emails, photo = photo, user_name = username, password = password, role = role)
                              customer=Hotel.objects.create(hotel_name = hotel_name, username = username, password = password, address = address, place = place,emails = emails, phone = phone, photo = photo, role = role)
                              customer.save()
                              error = 'no'
                        else:
                              error = 'yes'
                  except:
                        error = 'yes'
      content = {'error':error}
      return render(request,'hotels/hotel_signup.html',content)

# def hotel_login(request):

#       if request.method == "POST":
#             username = request.POST['username']
#             password = request.POST['password']

#             # customer = auth.authenticate(username = username, password = password)
#             # print("===============================", username, password)

#             # customers = Hotel.objects.filter(username=username,password=password,approved=True)
#             # if customers is not None:
#             #       if customers.exists():
#             #             auth.login(request,customer)
#             #             return redirect(hotel_dashboard)      
#             # else:
#             #       messages.info(request,"your account is not approved! Please wait.")
#             #       return redirect(hotel_login)

#             try:
#             # Query the database for the hotel user with the provided username and password
#                   hotel = Hotel.objects.get(username=username, password=password, approved=True)
#                   # print("===================================",username, password)
#             except Hotel.DoesNotExist:
#             # Hotel user with the provided credentials or approval status does not exist
#                   messages.error(request, "Invalid credentials or account not approved.")
#                   return redirect('hotel_login')

#         # If hotel user exists and is approved, log in the user
#             if hotel.role == 'HOTEL':
#                   request.session['hotel_id'] = hotel.id
#                   print("===================================",hotel.id)
#                   return redirect('hotel_dashboard')
#       return render(request,'hotels/hotel_login.html')


def hotel_login(request):
      if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            try:
                  hotel = Hotel.objects.get(username=username, password = password, approved = True)

                  # Set session variable for authenticated hotel user
                  request.session['hotel_id'] = hotel.id
                  return redirect('hotel_dashboard')
      
            except Hotel.DoesNotExist:
                  messages.error(request, "Invalid credentials or account not approved.")
    
      return render(request, 'hotels/hotel_login.html')


@login_required
def hotel_dashboard(request):
    if 'hotel_id' in request.session:
        hotel_id = request.session['hotel_id']
        try:
            hotel = Hotel.objects.get(id=hotel_id)
            customers = Customer.objects.all()
            return render(request, 'hotels/hotel_home.html', {'customers': customers, 'hotel': hotel})
        except Hotel.DoesNotExist:
            # Handle case where hotel with given ID does not exist
            del request.session['hotel_id']
    
    # Redirect to login page if user is not authenticated
    return redirect('hotel_login')



# @login_required
# def hotel_view_customers(request):
#       customers = Customer.objects.all()
#       return render(request,"admin/admin_view_customers.html", {'customers':customers})

def add_hotel_room(request):
      # hotels = Hotel.objects.get(id = hotel_id)
      # print("===================================",hotels)
      if request.method == "POST":
           room_number = request.POST['room_number']
           capacity = request.POST['capacity']
           number_of_beds = request.POST['number_of_beds']
           room_type = request.POST['room_type']
           price = request.POST['price']
           floor_number = request.POST['floor_number']
           photo = request.FILES.get('photo')
      #      hotel = Hotel.objects.get(id=id)
           print("==============================================",room_number,capacity,number_of_beds,room_type)

           rooms = Room.objects.create(room_number = room_number, capacity = capacity, number_of_beds = number_of_beds, room_type = room_type, price = price, floor_number = floor_number, photo = photo)
           rooms.save()

           return redirect('hotels_view_room_details')
      return render(request,'hotels/add-hotel-rooms.html')

def hotels_view_room_details(request):
      return render(request,'hotels/hotels_view_room_details.html')
