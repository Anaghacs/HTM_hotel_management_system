from django.shortcuts import render,redirect
from django.contrib import messages,auth
from django.contrib.auth.models import User
# from .models import Hotels
from django.contrib.auth.hashers import make_password

def hotel_login(request):
      if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']

            user = auth.authenticate(username = username, password = password)
            print("=============================",user)


            if user is not None:
                  auth.login(request, user)

                  if user.approved == True:              
                        return redirect('/')
                  
                  else:
                        messages.error("Your account has been not approved by the admin! Please wait !")


            else:
                  messages.info("No such user! Please signup for the website")
                  return redirect('user_signup') 
                  


# Create your views here.
def hotel_signup(request):
      if request.method == "POST":
            hotel_name = request.POST['hotel_name']
            address = request.POST['address']
            place = request.POST['place']
            phone = request.POST['phone']
            email = request.POST['email']
            username = request.POST['username']
            password = request.POST['password1']
            print("==================================",hotel_name, email, username, password)

            #photo file get
            photo = request.FILES.get('photo') 
            print("--------------------------",photo)
            
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
                  #create hotel model and insert the data
                  hotels = Hotels.objects.create(hotel_name = hotel_name, address = address, place = place, phone = phone, email = email, photo = photo, user_name = username, password = password)
                  hotels.save()
                  return redirect('logins')
      return render(request,'hotels/hotel_signup.html')

def hotel_home(request):
      return render(request, 'hotels/hotel_home.html')