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

def hotel_login(request):

      if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']

            # customer = auth.authenticate(username = username, password = password)
            # print("===============================", username, password)

            # customers = Hotel.objects.filter(username=username,password=password,approved=True)
            # if customers is not None:
            #       if customers.exists():
            #             auth.login(request,customer)
            #             return redirect(hotel_dashboard)      
            # else:
            #       messages.info(request,"your account is not approved! Please wait.")
            #       return redirect(hotel_login)

            try:
            # Query the database for the hotel user with the provided username and password
                  hotel = Hotel.objects.get(username=username, password=password, approved=True)
                  # print("===================================",username, password)
            except Hotel.DoesNotExist:
            # Hotel user with the provided credentials or approval status does not exist
                  messages.error(request, "Invalid credentials or account not approved.")
                  return redirect('hotel_login')

        # If hotel user exists and is approved, log in the user
            if hotel.role == 'HOTEL':
                  request.session['hotel_id'] = hotel.id
                  return redirect('hotel_dashboard')
      return render(request,'hotels/hotel_login.html')


# def hotel_login(request):
#       return render(request,'hotels/hotel_login.html')


# @login_required
def hotel_dashboard(request):

      customers = Customer.objects.all()
      return render(request,'hotels/hotel_home.html',{'customers':customers})

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
# def hotel_logout(request):
#       logout(request)
#       return redirect('index')

# def edit_hotel_profile(request,id):

#       hotel = Hotel.objects.get(id = id)
#       if request.method == 'POST':
#             hotelname = request.POST.get('hotelname')

#       return render(request,'hotels/hotel-profile-edit.html')



# def edit_hotel_details(request,id):
#     hotel = Hotel.objects.get(id = id)  # Assuming each user is associated with one hotel
#     error = ""
#     if request.method == 'POST':
#         # Extract form data
#         hotel.hotel_name = request.POST.get('hotel_name')
#         hotel.username = request.POST.get('username')
#         hotel.password = request.POST.get('password')
#         hotel.address = request.POST.get('address')
#         hotel.place = request.POST.get('place')
#         hotel.emails = request.POST.get('emails')
#         hotel.phone = request.POST.get('phone')
#         # Assuming 'photo' is the name attribute of the file input field for the photo
#         hotel.photo = request.FILES.get('photo')
#         hotel.role = request.POST.get('role')
        
#         try:
#             hotel.save()
#             # Redirect to a success page or back to the hotel profile page
#             return redirect('success_url')
#         except:
#             error = 'An error occurred while saving the hotel details.'

#     return render(request, 'hotels/hotel-profile-edit.html', {'hotel': hotel, 'error': error})