from django.shortcuts import render,redirect
from django.contrib import messages,auth
from home.models import Hotel,User,Customer
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render,redirect

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
      print("===============================")
      if request.method == "POST":
            print("===============================")
            username = request.POST['username']
            password = request.POST['password']

            customer = auth.authenticate(username = username, password = password)

            print("===============================",username,password)
            customers = Hotel.objects.filter(username=username,password=password,approved=True)

            if customers.exists():
                        auth.login(request,customer)
                        return redirect(hotel_dashboard)      
            else:
                  messages.info(request,"your account is not approved! Please wait.")
                  return redirect(hotel_login)
            
                  # messages.info(request,"Username and password is not registered! Please signup first.")      
      return render(request,'hotels/hotel_login.html')

def hotel_dashboard(request):
       return render(request,'hotels/hotel_home.html')

