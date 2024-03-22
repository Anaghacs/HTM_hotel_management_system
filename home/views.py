from django.shortcuts import render,redirect
from django.contrib import messages,auth
from home.models import Hotel, Customer 
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

# # Create your views here.

def index(request):
      hotels = Hotel.objects.all()
      # facilities = Facilities.objects.filter(hotels = hotels)

      return render(request,'commons/indexs.html', {'hotels' : hotels, })

def login_admin(request):
      print("===============================")
      if request.method == "POST":
            print("===============================")
            username = request.POST['username']
            password = request.POST['password']

            customers = auth.authenticate(username = username, password = password)
            
            print("===============================",username,password)
            # customer =Customer.objects.get(username = username, password = password)
            print("+++++++++++++============",customers)

            if customers is not None:
                  if customers.role == 'ADMIN':
                        auth.login(request,customers)
                        return redirect(admin_home)        
            else:
                  messages.info(request,"Username and password is not registered! Please signup first.")  
      return render(request,'admin/admin_login.html')


@login_required
def admin_home(request):
      # Fetch the currently logged-in user
      current_user = request.user

    # Assuming the username is stored in a field called 'username'
      admin_username = current_user.username

      hotels = Hotel.objects.all()
      # users = Customer.objects.all()
      return render(request,'admin/admin-dashboard.html',{'hotels' : hotels, 'admin_username' : admin_username})


@login_required
def admin_view_hotel(request):
      current_user = request.user

      admin_username = current_user.username
      hotels = Hotel.objects.all()
      return render(request,'admin/admin-view-hotel.html',{'hotels' : hotels, 'admin_username' : admin_username})


@login_required
def approve(request,id):
      
      hotels = get_object_or_404(Hotel , id = id)
      hotels.approved = True
      hotels.save()
      return redirect('admin_view_hotel')


@login_required
def block(request,id):
      hotels= get_object_or_404(Hotel, id = id)
      hotels.approved = False
      hotels.save()
      return redirect('admin_view_hotel')


@login_required
def approve_view_hotels(request):
      current_user = request.user

      admin_username = current_user.username

      hotels = Hotel.objects.filter(approved = True)
      return render(request,"admin/admin_view_approved_hotels.html",{'hotels' : hotels, 'admin_username' : admin_username})


@login_required
def admin_view_customers(request):
      current_user = request.user

      admin_username = current_user.username
      customers = Customer.objects.all()
      return render(request,"admin/admin_view_customers.html", {'customers' : customers, 'admin_username' : admin_username})


@login_required
def admin_logout(request):
      logout(request)
      return redirect('index')