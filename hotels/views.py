from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import Hotels

# Create your views here.
def hotel_signup(request):
      if request.method == "POST":
            hotel_name = request.POST['hotel_name']
            address = request.POST['address']
            place = request.POST['place']
            phone = request.POST['phone']
            email = request.POST['email']
            print("==================================",hotel_name, email)

            #photo file get
            photo = request.FILES.get('photo') 
            print("--------------------------",photo)

            #create hotel model and insert the data
            hotels = Hotels.objects.create(hotel_name = hotel_name, address = address, place = place, phone = phone, email = email, photo = photo)
            hotels.save()
            return redirect('logins')
      return render(request,'hotels/hotel_signup.html')

def hotel_home(request):
      return render(request, 'hotels/hotel_home.html')