from django.shortcuts import render, HttpResponse,redirect
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import UserProfile
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import logout
from .models import FoodItem
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST, require_http_methods
from .forms import FoodItemSearchForm
from django.db.models import Q
import random
from django.core.files.storage import FileSystemStorage




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

@login_required(login_url='SignInPage')
def EditProfile(request):
    return render(request, 'EditAcc.html')

@login_required(login_url='SignInPage')
def MyAccount(request):
    # Get the user's data from the database
    user_data = {
        'name': request.user.get_full_name(),
        'email': request.user.email,
        'username': request.user.username,
    }
    return render(request, 'Account.html', {'user_data': user_data})

@login_required
def update_account(request):
    if request.method == 'POST':
        # Retrieve the user's data from the form
        new_fullname = request.POST.get('fullname')
        new_username = request.POST.get('name')
        new_email = request.POST.get('email')
        new_phone = request.POST.get('phone')
        new_password = request.POST.get('password')
        
        # Update the user's data in the database (you should perform validation and error handling here)
        user = request.user
        user.fullname = new_fullname
        user.username = new_username
        user.email = new_email
        user.phone = new_phone
        
        if new_password:
            user.set_password(new_password)
        
        user.save()
        
        # Redirect to the user's profile page (you can change the URL as needed)
        return redirect('/MyAccount')
    
    # Handle GET requests or errors
    # You may want to add error handling for invalid POST requests here
    
    # Render a template if needed
    return render(request, 'update_account.html')

@login_required(login_url='SignInPage')
def DeleteAccount(request):
    if request.method == 'POST':
        # Delete the user's data here
        user = request.user
        user.delete()
        logout(request)
        messages.success(request, "Your account has been deleted successfully.")
        return redirect('SignUpPage')
    
    return render(request, 'delete_account.html')

def categories_view(request):
    # Add logic to retrieve and display categories
    categories = []  # Replace with your actual categories data or logic
    return render(request, 'categories.html', {'categories': categories})

def add_food(request):
    if request.method == 'POST':
        food_name = request.POST.get('food-name')
        food_ingredients = request.POST.get('food-ingredients')
        food_category = request.POST.get('food-category')
        food_image = request.FILES.get('food-image')
        food_description = request.POST.get('food-description')  # Retrieve the description field

        new_food_item = FoodItem(
            name=food_name,
            ingredients=food_ingredients,
            category=food_category,
            image=food_image,
            description=food_description,  # Assign the description to the 'description' field
        )
        new_food_item.save()

        return redirect('food_list') # Replace with the appropriate URL name

    # If not a POST request, render the food categorization page with existing data
    categories = []  # Replace with your categories data
    food_items = FoodItem.objects.all()  # Retrieve food items from the database

    return render(request, 'categories.html', {'categories': categories, 'food_items': food_items})

def food_list(request):
    food_items = FoodItem.objects.all()  # Retrieve all food items from the database
    return render(request, 'categories.html', {'food_items': food_items})


@require_http_methods(["DELETE"])
def delete_food_item(request, item_id):
    try:
        # Get the FoodItem object to delete
        food_item = get_object_or_404(FoodItem, id=item_id)

        # Delete the object from the database
        food_item.delete()

        # Return a 204 (No Content) response, indicating success
        return JsonResponse({'message': 'Food item deleted successfully'}, status=204)
    except Exception as e:
        # Handle any exceptions or errors
        return JsonResponse({'message': 'Failed to delete food item', 'error': str(e)}, status=400)

@require_POST
def update_food_item(request, item_id):
    # Get the FoodItem object to update
    food_item = get_object_or_404(FoodItem, id=item_id)

    # Update the attributes based on the form data
    food_item.name = request.POST.get('edit-food-name')
    food_item.description = request.POST.get('edit-food-description')
    food_item.ingredients = request.POST.get('edit-food-ingredients')
    food_item.category = request.POST.get('edit-food-category')
    food_image = request.FILES.get('edit-food-image')  # Retrieve the uploaded image

    if food_image:  # Check if a new image was uploaded
        food_item.image = food_image  # Assign the uploaded image to the 'image' field

    # Validate the updated object
    try:
        food_item.full_clean()
    except ValidationError as e:
        return JsonResponse({'message': 'Invalid form data', 'errors': e.message_dict}, status=400)

    # Save the updated object to the database
    food_item.save()

    return JsonResponse({'message': 'Food item updated successfully'})

def category_search(request):
    form = FoodItemSearchForm(request.GET)
    results = []

    if form.is_valid():
        search_query = form.cleaned_data['search_query']
        results = FoodItem.objects.filter(name__icontains=search_query)

    return render(request, 'food_item_search_results.html', {'form': form, 'results': results})

def food_item_search_results(request):
    search_query = request.GET.get('search_query', '')
    filter_category = request.GET.get('filter_category', 'all')

    if search_query:
        # Create a base query that matches the search query in name or ingredients
        base_query = Q(name__icontains=search_query) | Q(ingredients__icontains=search_query)

        if filter_category == 'all':
            results = FoodItem.objects.filter(base_query)
        elif filter_category == 'healthy':
            results = FoodItem.objects.filter(base_query, category='Healthy')
        elif filter_category == 'unhealthy':
            results = FoodItem.objects.filter(base_query, category='Unhealthy')
    else:
        if filter_category == 'all':
            results = FoodItem.objects.all()
        elif filter_category == 'healthy':
            results = FoodItem.objects.filter(category='Healthy')
        elif filter_category == 'unhealthy':
            results = FoodItem.objects.filter(category='Unhealthy')

    return render(request, 'foodItemSearchResults.html', {'results': results, 'search_query': search_query})

def random_item(request):
    # Get a random item from the database
    random_item = FoodItem.objects.order_by('?').first()
    
    context = {
        'random_item': random_item
    }
    return render(request, 'randomItem.html', context)

def display_food_items(request):
    # Query your database to get the list of food items
    food_items = FoodItem.objects.all()  # Change this query to match your model

    return render(request, 'DisplayFoodItems.html', {'food_items': food_items})


def categories_view(request):
    food_items = FoodItem.objects.all()
    return render(request, 'categories.html', {'food_items': food_items})

def item_page(request, item_id):
    # Retrieve the FoodItem object with the given item_id
    item = FoodItem.objects.get(pk=item_id)

    # Pass the item to the template
    context = {
        'item': item,
    }

    return render(request, 'itemPage.html', context)
