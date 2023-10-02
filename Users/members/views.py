from django.shortcuts import render, HttpResponse,redirect
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required(login_url='SignInPage')
def LandingPage(request):
  return render (request,'LandingPage.html')

@login_required(login_url='SignInPage')
def HomePage(request):
  return render (request,'homePage.html')

def SignUpPage(request):
  if request.method=='POST':
    fname=request.POST.get('fname')
    uname=request.POST.get('username')
    email=request.POST.get('email')
    pnum=request.POST.get('phoneNum')
    pass1=request.POST.get('pass1')
    pass2=request.POST.get('pass2')
    gender=request.POST.get('gender')

    # Check if the username already exists
    if User.objects.filter(username=uname).exists():
      messages.error(request, "Username already exists. Please choose a different username.")
      username_exists = "True"
      return redirect('SignUpPage')  # Redirect back to the signup page with an error message
 
    if pass1!=pass2:
      messages.error(request, "Your Password and Confirm Password are not the same!")
      return redirect('SignUpPage')  # Redirect back to the signup page with an error message
      
    else:
       # Create the User instance
      my_user=User.objects.create_user(uname,email,pass1)
      my_user.save()

       # Create the UserProfile instance
      user_profile = UserProfile(full_name=fname, username=uname, email=email, phone_number=pnum, password=pass1, gender=gender)
      user_profile.save()

      return redirect('SignInPage')

  return render (request,'SignUp.html')

def Nutritionist(request):
  return render (request,'SignUpNutri.html')

def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('password')
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('HomePage')
        else:
            messages.error(request, 'Username or Password is incorrect!')
            # Add a variable to indicate authentication failure
            auth_failed = True
    else:
        auth_failed = False  # Set it to False by default

    return render(request, 'LogIn.html', {'auth_failed': auth_failed})

@login_required(login_url='SignInPage')
def MyAccount(request):
  return render (request,'Account.html')

def SignOut(request):
    logout(request)
    return redirect('SignInPage')