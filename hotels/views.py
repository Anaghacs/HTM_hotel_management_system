from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from home.models import Hotel, User, Customer, Room, Facilities, Booking, Order
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

def hotel_signup(request):
    if request.method == "POST":
        hotel_name = request.POST['hotel_name']
        username = request.POST['username']
        password = request.POST['password']
        address = request.POST['address']
        place = request.POST['place']
        emails = request.POST['emails']
        phone = request.POST['phone']
        role = request.POST['role']

            # delete set ay epo epo signup anu isue ok
        # photo file get
        photo = request.FILES.get('photo')
        print("==================================",hotel_name, emails, username, password,phone,role,place,photo)


        # Checking for empty or whitespace inputs
        if not hotel_name.strip():
            messages.error(request, "Hotel name cannot be empty or whitespace.")
            return redirect('hotel_signup')
        elif not address.strip():
            messages.error(request, "Address cannot be empty or whitespace.")
            return redirect('hotel_signup')
        elif not place.strip():
            messages.error(request, "Place cannot be empty or whitespace.")
            return redirect('hotel_signup')

        try:
            # Create hotel model and insert the data
            if role == "HOTEL":
                # It's better to use create() directly instead of creating an object and then saving it
                customer = Hotel.objects.create(
                    hotel_name = hotel_name,
                    username = username,
                    password = password,
                    address = address,
                    place = place,
                    emails = emails,
                    phone = phone,
                    photo = photo,
                    role = role
                )
                messages.success(request, "Signup successful. You can now login.")
                return redirect('hotel_login')
        except Exception as e:
            messages.error(request, f"Signup failed: {str(e)}")
            return redirect('hotel_signup')

    return render(request, 'hotels/hotel_signup.html')


# def hotel_signup(request):
#       error = ""
#       if request.method == "POST":
            
#             hotel_name = request.POST['hotel_name']
#             username = request.POST['username']
#             password = request.POST['password']
#             address = request.POST['address']
#             place = request.POST['place']
#             emails = request.POST['emails']
#             phone = request.POST['phone']

#             #photo file get
#             photo = request.FILES.get('photo')
#             role = request.POST['role']
#             print("==================================",hotel_name, emails, username, password)

            
#             if hotel_name == "" or hotel_name == " ":
#                   messages.info(request,"hotelname is not allowed space and blank space and not allowed special characters")
#                   return redirect(hotel_signup)
            
#             elif address == "" or address == "":
#                   messages.info(request,"address is not allowed space and blank space and not allowed special characte")
#                   return redirect(hotel_signup)
            
            
#             elif place == "" or place == "":
#                   messages.info(request,"place is not allowed space and blank space and special character")
#                   return redirect(hotel_signup)
            
#             else:
#                   try:
#                   #create hotel model and insert the data
#                         if role == "HOTEL":
                              
#                               customer = Hotel.objects.create(hotel_name = hotel_name, username = username, password = password, address = address, place = place,emails = emails, phone = phone, photo = photo, role = role)
#                               customer.save()
#                               error = 'no'
#                         else:
#                               error = 'yes'
#                   except:
#                         error = 'yes'
#       content = {'error':error}
#       return render(request,'hotels/hotel_signup.html',content)


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


# @login_required
def logout(request):
    # Clear the session data
    request.session.flush()
    # Redirect to the login page or any other desired page
    return redirect('index')

# @login_required
def hotel_dashboard(request):
    if 'hotel_id' in request.session:
        hotel_id = request.session['hotel_id']
        try:
            hotel = Hotel.objects.get(id = hotel_id)
            customers = Customer.objects.all()
            return render(request, 'hotels/hotel_home.html', {'customers': customers, 'hotel': hotel})
        except Hotel.DoesNotExist:
            # Handle case where hotel with given ID does not exist
            del request.session['hotel_id']
    
    # Redirect to login page if user is not authenticated
    return redirect('hotel_login')

@login_required
def add_hotel_room(request):
      print("===========================================hiiiiiiiiiii")
      if 'hotel_id' in request.session:
        
            hotel_id = request.session['hotel_id']
            print("=============================================",hotel_id)
            # hotel = Hotel.objects.get(id=hotel_id)
            hotel = get_object_or_404(Hotel, id = hotel_id)

            print("==============================",hotel.hotel_name)

            if request.method == "POST":
            
                  room_number = request.POST['room_number']
                  capacity = request.POST['capacity']
                  number_of_beds = request.POST['number_of_beds']
                  room_type = request.POST['room_type']
                  price = request.POST['price']
                  floor_number = request.POST['floor_number']
                  photo = request.FILES.get('photo')

                  print("========================================",hotel.hotel_name, room_number,capacity,number_of_beds,room_type,price)
                  room = Room.objects.create(
                        hotel = hotel,
                        room_number = room_number,
                        capacity = capacity,
                        number_of_beds = number_of_beds,
                        room_type = room_type,
                        price = price,
                        floor_number = floor_number,
                        photo = photo
                  )
                  room.save()
                  messages.success(request, "Your room record has been successfully added!")

                  return redirect('hotels_view_room_details')
            
      return render(request, 'hotels/add-hotel-rooms.html', {'hotel': hotel})


# @login_required
def hotels_view_room_details(request):

      if 'hotel_id' in request.session:
            hotel_id = request.session['hotel_id']
            # hotel = Hotel.objects.get(id = hotel_id)
            hotel = get_object_or_404(Hotel, id = hotel_id)

            print("================================",hotel.hotel_name)
            rooms = Room.objects.filter(is_deleted = False, hotel = hotel)
            print("==========================================",rooms)
      return render(request,'hotels/hotels_view_room_details.html', {'rooms' : rooms, 'hotel' : hotel})


@login_required
def delete_room(request, room_number):
      print("right plase")
      if 'hotel_id' in request.session:
            hotel_id = request.session['hotel_id']
            try:
                  hotel = Hotel.objects.get(id = hotel_id)
                  print("===========================",hotel.hotel_name)
                  room = get_object_or_404(Room, room_number = room_number)
                  print("===========================",room.room_number)
                  room.is_deleted = True
                  room.save()
                  messages.success(request, "Your record has been successfully deleted!")

            except Hotel.DoesNotExist:
            # Handle the case where the hotel with the given ID doesn't exist
                  pass
      return redirect('hotels_view_room_details')


@login_required
def update_room_details(request, room_number):
      if 'hotel_id' in request.session:
            hotel_id = request.session['hotel_id']
            hotel = get_object_or_404(Hotel, id = hotel_id)
            
            room = get_object_or_404(Room, room_number = room_number)
            return render(request, 'hotels/update-hotel-room.html', {'room': room, 'hotel' : hotel})


@login_required     
def update_rooms(request, room_number):
    # Check if 'hotel_id' exists in the session
    if 'hotel_id' in request.session:
        hotel_id = request.session['hotel_id']
        hotel = get_object_or_404(Hotel, id=hotel_id)

        # Check if the request method is POST
        if request.method == "POST":
            # Get the room details from the POST data
            capacity = request.POST.get('capacity')
            number_of_beds = request.POST.get('number_of_beds')
            room_type = request.POST.get('room_type')
            price = request.POST.get('price')
            floor_number = request.POST.get('floor_number')
            photo = request.FILES.get('photo')

            # Get the room object to update
            room = get_object_or_404(Room, room_number=room_number)

            # Update room details
            room.capacity = capacity
            room.number_of_beds = number_of_beds
            room.room_type = room_type
            room.price = price
            room.floor_number = floor_number

            if photo:
                room.photo = photo

            room.save()
            messages.success(request, "Your record has been successfully updated!")
            return redirect('hotels_view_room_details')

        else:
            messages.error(request, "Missing field in the request.")
            # Redirect or render a response indicating the error

    else:
        # Handle case where 'hotel_id' is not in session
        # Redirect or render a response indicating the error
        messages.error(request, "Hotel ID not found in session.")

    return render(request, 'hotels/hotels_view_room_details.html', {'hotel': hotel})

#add hotel facilities
@login_required
def add_hotel_facilities(request):
      if 'hotel_id' in request.session:
            hotel_id = request.session['hotel_id']
            hotel = get_object_or_404(Hotel, id = hotel_id)

            if request.method == "POST":
            
                  facility = request.POST['facility']
                  description = request.POST['description']
                  photo = request.FILES.get('photo')

                  facilities = Facilities.objects.create(
                        hotel = hotel,
                        facility = facility,
                        description = description,
                        photo = photo
                  )
                  facilities.save()
                  messages.success(request, "Your record has been successfully added!")

                  return redirect('hotel_view_facilities')
                  
      return render(request, "hotels/add-hotel-facilities.html", {'hotel': hotel})

def hotel_view_facilities(request):
      if 'hotel_id' in request.session:
            hotel_id = request.session['hotel_id']
            hotel = Hotel.objects.get(id = hotel_id)
            print("================================",hotel.hotel_name)
            facilities = Facilities.objects.filter(is_deleted = False, hotel = hotel)
      return render(request, "hotels/hotel-view-facilities.html",{'facilities' : facilities, 'hotel': hotel})


def hotel_delete_facilities(request, id):
      if 'hotel_id' in request.session:
            hotel_id = request.session['hotel_id']
            try:
                  # hotel = Hotel.objects.get(id = hotel_id)
                  hotel = get_object_or_404(Hotel, id = hotel_id)
                  print("===========================",hotel.hotel_name)
                  facilities = get_object_or_404(Facilities, id = id)
                  facilities.is_deleted = True
                  facilities.save()
                  messages.success(request, "Your record has been successfully deleted!")

            except Hotel.DoesNotExist:
            # Handle the case where the hotel with the given ID doesn't exist
                  pass
      return redirect('hotel_view_facilities',{'hotel' : hotel})


def hotel_update_facilities(request, id):
      if 'hotel_id' in request.session:
            hotel_id = request.session['hotel_id']
            hotel = get_object_or_404(Hotel, id = hotel_id)
            print("============================", hotel.hotel_name) 

            facilities = get_object_or_404(Facilities, id = id)
            return render(request, 'hotels/update-hotel-facilities.html', {'facilities': facilities, 'hotel' : hotel})


def update_facilities(request, id):
      if 'hotel_id' in request.session:
        hotel_id = request.session['hotel_id']
        hotel = get_object_or_404(Hotel, id=hotel_id)
        print("============================", hotel.hotel_name) 

        if 'facility' in request.POST and 'description' in request.POST:
            facility = request.POST['facility']
            description = request.POST['description']
            photo = request.FILES.get('photo')

            facilities = get_object_or_404(Facilities, id=id)
            
            facilities.facility = facility
            facilities.description = description

            if photo:
                facilities.photo = photo

            facilities.save()
            messages.success(request, "Your record has been successfully updated!")
            return redirect('hotel_view_facilities')
        else:
            messages.error(request, "Missing facility or description in the request.")
            # Redirect or render a response indicating the error
        # Handle case where 'hotel_id' is not in session
      return render(request, 'hotels/hotel-view-facilities.html')


def room_availability(request):
     return render(request, 'hotels/room_availability.html')

def room_booking_details(request):
     if 'hotel_id' in request.session:
            hotel_id = request.session['hotel_id']
            hotel = Hotel.objects.get(id = hotel_id)
            print("===============================",hotel.hotel_name)
            booking = Booking.objects.filter(room__hotel=hotel)
            order = Order.objects.filter(hotel = hotel)
            room = Room.objects.filter(hotel= hotel)
            # brooo oru help cheyo addhym edit and delete button onu set ako ath wrk ayirunatha epo wrk avunila ok evide kanikk ok ithanoo isyes ok ithu auth login ann googlint aa buttons edukk auth login ala session use cheythit anu but delete anunud en thonunu but vere page lek pokunu nk modal varanam anit yes button il click cheyombo delete avanam html page edukk

     return render(request, 'hotels/room_booking_details.html', {'hotel' : hotel, 'order' : order, 'booking' : booking, 'room' : room})