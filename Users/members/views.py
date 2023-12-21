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
from .models import FoodItem, Review
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST, require_http_methods
from .forms import FoodItemForm, FoodItemSearchForm, ReviewForm
from django.db.models import Q
import random
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse
from .models import Appointment
from . import models
from django.db.models import TextField
from .models import AdminProfile





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
    try:
        # Try to get the user's profile data
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # If the profile does not exist, create an empty profile
        user_profile = UserProfile()

 

    # Get the user's basic data from the database
    user_data = {
        'name': request.user.get_full_name(),
        'email': request.user.email,
        'username': request.user.username,
    }

    print("User Data:", user_data)

    return render(request, 'Account.html', {'user_data': user_data, 'user_profile': user_profile})



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
    num_random_items = 4
    random_items = FoodItem.objects.order_by('?')[:num_random_items]
   

    context = {
        'food_items': random_items
    }
    return render(request, 'homePage.html', context)

def display_food_items(request):
    # Query your database to get the list of food items
    food_items = FoodItem.objects.all()  # Change this query to match your model

    return render(request, 'DisplayFoodItems.html', {'food_items': food_items})


def categories_view(request):
    food_items = FoodItem.objects.all()
    return render(request, 'categories.html', {'food_items': food_items})


@login_required(login_url='SignInPage')
def item_page(request, item_id):
    item = get_object_or_404(FoodItem, pk=item_id)

    # Handle the review form submission
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.food_item = item
            review.save()
            messages.success(request, 'Your review has been submitted.')

    # Fetch existing reviews for the item
    reviews = Review.objects.filter(food_item=item)

    context = {
        'item': item,
        'form': ReviewForm(),  # Create an instance of the ReviewForm
        'reviews': reviews,
    }

    return render(request, 'itemPage.html', context)


@login_required(login_url='SignInPage')
def edit_review(request, item_id, review_id):
    review = get_object_or_404(Review, id=review_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Review updated successfully.')
            return HttpResponseRedirect(reverse('item_page', args=[item_id]))
    else:
        form = ReviewForm(instance=review)

    context = {
        'form': form,
        'review_id': review.id,
    }

    return render(request, 'edit_review.html', context)


@login_required(login_url='SignInPage')
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    if request.method == 'POST':
        food_item_id = None
        if review.food_item:
            food_item_id = review.food_item.id
            review.delete()
            messages.success(request, 'Review deleted successfully.')
        else:
            messages.error(request, 'Error deleting review.')

        if food_item_id:
            return redirect('item_page', item_id=food_item_id)

    context = {
        'review': review,
    }

    return render(request, 'delete_review.html', context)

def healthy_foods(request):
    # Retrieve healthy foods from your database or any other source
    healthy_foods_list = FoodItem.objects.filter(category='Healthy')
    context = {'foods': healthy_foods_list}
    return render(request, 'HealthyFood.html', context)

def unhealthy_foods(request):
    # Retrieve unhealthy foods from your database or any other source
    unhealthy_foods_list = FoodItem.objects.filter(category='unhealthy')
    context = {'foods': unhealthy_foods_list}
    return render(request, 'UnhealthyFood.html', context)

def schedule_appointment(request):
    # Handle appointment scheduling logic here
    # For example, you might render a form to schedule an appointment
    return render(request, 'schedule_appointment.html')

def schedule_appointment(request):
    if request.method == 'POST':
        # Retrieve form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        date = request.POST.get('date')
        time = request.POST.get('time')
        purpose = request.POST.get('purpose')  # Retrieve the purpose from the form

        # Create an Appointment object and save it to the database
        appointment = Appointment.objects.create(
            user=request.user,  # Assuming you're using authentication and the user is logged in
            name=name,
            email=email,
            date=date,
            time=time,
            purpose=purpose,  # Assign the purpose from the form data
        )

         # Redirect to a success page or wherever you want
        messages.success(request, 'Appointment is set successfully') # Redirect to a success URL

    return render(request, 'schedule_appointment.html') 

def AdminSignUpPage(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pnum = request.POST.get('phoneNum')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        gender = request.POST.get('gender')

        # Check if the username already exists
        if User.objects.filter(username=uname).exists():
            messages.error(request, "Username already exists. Please choose a different username.")
            return redirect('AdminSignUp')  # Redirect back to the signup page with an error message

        # Check if passwords match
        if pass1 != pass2:
            messages.error(request, "Your Password and Confirm Password are not the same!")
            return redirect('AdminSignUp')  # Redirect back to the signup page with an error message

        # Create the User instance
        my_user = User.objects.create_user(username=uname, email=email, password=pass1)

        # Create the AdminProfile instance
        admin_profile = AdminProfile(full_name=fname, username=uname, email=email, phone_number=pnum, password=pass1, gender=gender)
        admin_profile.save()

        return redirect('AdminLogin')

    return render(request, 'adminSignUp.html')

def adminLogin(request):
    if request.method == 'POST':
        # Handle admin login logic here
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the admin user
        admin_user = authenticate(request, username=username, password=password)

        if admin_user is not None:
            # Login the admin user
            login(request, admin_user)
            return redirect('AdminPage')  # Redirect to the admin dashboard
        else:
            messages.error(request, 'Admin login failed. Please check your credentials.')

    return render(request, 'AdminLogin.html')

@login_required(login_url='AdminLogin')  # Redirect to admin login page if not authenticated
def admin_dashboard(request):
    # Admin dashboard logic goes here
    return render(request, 'AdminPage.html')

def choose_login(request):
    return render(request, 'ChooseLogin.html')

@login_required(login_url='SignInPage')
def AppointmentStatus(request):
    # Filter appointments based on the current user
    appointments = Appointment.objects.filter(user=request.user)

    return render(request, 'AppointmentStatus.html', {'appointments': appointments})

def adminPage(request):
    # Get all users
    all_users = User.objects.all()

    # Check if a user_id is provided for editing or deleting
    user_id = request.GET.get('user_id')
    if user_id:
        # Get the user and user profile
        user = User.objects.get(id=user_id)
        user_profile = UserProfile.objects.get(user=user)

        # Handle delete action
        if request.method == 'POST' and request.POST.get('action') == 'delete':
            user.delete()
            return redirect('AdminPage')

        # Handle edit action
        elif request.method == 'POST' and request.POST.get('action') == 'edit':
            # Update user profile data (you can add validation)
            user_profile.full_name = request.POST.get('full_name')
            user_profile.phone_number = request.POST.get('phone_number')
            user_profile.gender = request.POST.get('gender')
            user_profile.save()

            # Redirect back to adminPage
            return redirect('adminPage')

        # Pass the user and user profile to the template for editing
        return render(request, 'adminPageEdit.html', {'user': user, 'user_profile': user_profile})

    # Pass all users to the template
    return render(request, 'AdminPage.html', {'all_users': all_users})

def adminPageDelete(request):
    try:
        if request.method == 'POST':
            selected_user_ids = request.POST.getlist('selected_users[]')

            if selected_user_ids:
                # Print selected user IDs for debugging
                print("Selected User IDs:", selected_user_ids)

                # Delete selected users
                User.objects.filter(id__in=selected_user_ids).delete()

        # Redirect back to the admin page after deletion
        return redirect('AdminPage')

    except Exception as e:
        # Print the exception for debugging
        print("Error:", e)
        return HttpResponseServerError("Internal Server Error")

@login_required(login_url='AdminLogin')
def adminPageEdit(request):
    return render(request, 'adminPageEdit.html')

def adminUpdateProfile(request):
    if request.method == 'POST':
        selected_user_ids = request.POST.getlist('selected_users[]')

        for user_id in selected_user_ids:
            try:
                user_profile = UserProfile.objects.get(user_id=user_id)

                new_fullname = request.POST.get(f'fullname_{user_id}')
                new_username = request.POST.get(f'username_{user_id}')
                new_email = request.POST.get(f'email_{user_id}')
                new_phone = request.POST.get(f'phone_{user_id}')
                new_password = request.POST.get(f'password_{user_id}')

                # Update user's data in the database
                user_profile.fullname = new_fullname
                user_profile.user.username = new_username
                user_profile.user.email = new_email
                user_profile.phone_number = new_phone

                if new_password:
                    user_profile.user.set_password(new_password)

                user_profile.user.save()
                user_profile.save()
            except UserProfile.DoesNotExist:
                # Handle the case where the user profile does not exist
                pass

        # Redirect after updating profiles
        return redirect('/AdminPage')

    # Handle GET requests or errors
    # You may want to add error handling for invalid POST requests here

    # Render a template if needed
    return render(request, 'update_account.html')
