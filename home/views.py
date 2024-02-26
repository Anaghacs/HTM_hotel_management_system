from django.shortcuts import render,redirect
from django.contrib import messages,auth
from home.models import Hotel,User,Customer
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout


# # Create your views here.

def index(request):
      return render(request,'commons/index.html')

def login_admin(request):
      print("===============================")
      if request.method == "POST":
            print("===============================")
            username = request.POST['username']
            password = request.POST['password']

            customer = auth.authenticate(username = username, password = password)
            
            print("===============================",username,password)
            # customer =Customer.objects.get(username = username, password = password)
            print("+++++++++++++============",customer)

            if customer is not None:
                  if customer.role == 'ADMIN':
                        auth.login(request,customer)
                        return redirect(admin_home)        
            else:
                  messages.info(request,"Username and password is not registered! Please signup first.")  
      return render(request,'admin/login_admin.html')

def admin_home(request):
      hotels = Hotel.objects.all()
      # users = Customer.objects.all()
      return render(request,'admin/admin-dashboard.html',{'hotels':hotels})

def admin_view_hotel(request):
      hotels = Hotel.objects.all()
      return render(request,'admin/admin-view-hotel.html',{'hotels':hotels})

def approve(request,id):
      print("++++++++++++++++++++++++++++++++======")

      hotels = Hotel.objects.get(id = id)
      print("++++++++++++++++++++++++++++++++======",hotels)
      
      print("==================================",hotels.approved)
      hotels.approved = True
      print("==================================",hotels.approved)

      # hotels.is_staff = True
      hotels.save()
      return render(request,"index.html")

# def view_hotels(request):
#       hotels = Hotel.objects.all()
#       return render(request, "admin_view_hotels.html",{'hotels':hotels})