from django.shortcuts import render,redirect
from django.contrib.auth.models import User

# Create your views here.
def hotel_signup(request):
      
      return render(request,'hotels/hotel_signup.html')