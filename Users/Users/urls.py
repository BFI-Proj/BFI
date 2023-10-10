"""
URL configuration for Users project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from members import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.LoginPage, name='SignInPage'),
    path('Home/', views.LandingPage, name='HomePage'),
    path('Food/', views.HomePage, name='FoodPage'),
    path('SignUp/', views.SignUpPage, name='SignUpPage'),
    path('SignUpNutri/', views.Nutritionist, name='SignUpNutri'),
    path('MyAccount/', views.MyAccount, name='MyAccountPage'),
    path('SignOut/', views.SignOut, name='SignOut'),
    path('edit_profile/', views.EditProfile, name='EditProfile'),
    path('update_account', views.update_account, name='update_account'),
    path('delete_account', views.DeleteAccount, name='DeleteAccount'),
    path('categories/', views.categories_view, name='categories'),
    path('add_food/', views.add_food, name='add_food'),
    path('food_list/', views.food_list, name='food_list'),
    path('delete_food_item/<int:item_id>/', views.delete_food_item, name='delete_food_item'),
    path('update_food_item/<int:item_id>/', views.update_food_item, name='update_food_item'),

    
    
]

