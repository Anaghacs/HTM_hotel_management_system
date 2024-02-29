from django.shortcuts import render,redirect
from django.contrib import messages,auth
from home.models import Hotel,User,Customer
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

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
      return render(request,'admin/page-account-login.html')

@login_required
def admin_home(request):
      hotels = Hotel.objects.all()
      # users = Customer.objects.all()
      return render(request,'admin/admin-dashboard.html',{'hotels':hotels})

@login_required
def admin_view_hotel(request):
      hotels = Hotel.objects.all()
      return render(request,'admin/admin-view-hotel.html',{'hotels':hotels})

@login_required
def approve(request,id):

      hotels = Hotel.objects.get(id = id)
      hotels.approved = True
      hotels.save()
      return render(request,"admin/admin_view_approved_hotels.html")

@login_required
def approve_view_hotels(request):

      hotels = Hotel.objects.filter(approved = True)
      return render(request,"admin/admin_view_approved_hotels.html",{'hotels':hotels})

@login_required
def admin_view_customers(request):
      customers = Customer.objects.all()
      return render(request,"admin/admin_view_customers.html", {'customers':customers})

@login_required
def admin_logout(request):
      logout(request)
      return redirect('index')