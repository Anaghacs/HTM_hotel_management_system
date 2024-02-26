from django.shortcuts import render,redirect
from django.contrib import messages,auth
from home.models import Hotel,User,Customer

# # Create your views here.

def index(request):
      return render(request,'commons/index.html')

def admin_login(request):
      print("===============================")
      if request.method == "POST":
            print("===============================")
            username = request.POST['username']
            password = request.POST['password']

            user = auth.authenticate(username = username, password = password)
            
            print("===============================",username,password)
            # customer =Customer.objects.get(username = username, password = password)
            print("+++++++++++++============",user)

            if user is not None:
                  if user.role == 'ADMIN':
                        auth.login(request,user)
                        return redirect(admin_home)        
            else:
                  messages.info(request,"Username and password is not registered! Please signup first.")  
      return render(request,'admin/admin_login.html')
def admin_home(request):
      return render(request,'admin/admin_dashboard.html')
