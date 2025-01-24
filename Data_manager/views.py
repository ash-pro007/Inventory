from django.shortcuts import render, redirect

from django.http import HttpResponse

from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout

import pandas as pd
from .models import Inventory, Product, Products_in_inventories




# Create your views here.


def login_page(request):
    return render(request, 'auth/login.html')


def signup(request):
    return render(request, 'auth/signup.html')


def home(request):
    return HttpResponse("Hello World Django")


def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
   
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

     
        if not username or not password1 or not password2:
            messages.error(request, 'All fields are required.')
            return render(request, 'signup.html')

        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'signup.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'signup.html')
        
        user = User.objects.create(
            username=username,
            password=make_password(password1) 
        )
        user.save()

        messages.success(request, 'Your account has been created successfully!')
        return redirect('login') 

    messages.success(request, 'Error! Couldn\'t create your account, please try again.')
    return render(request, 'signup.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

      
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
         
            return redirect('home') 
        else:
            messages.error(request, 'Invalid username or password.')
            return login_page(request)

    return login_page(request)


def home(request):
    if request.user.is_authenticated:

        is_user_admin = request.user.is_superuser
        return render(request, 'home.html', {'is_user_admin': is_user_admin})
    else:
        return redirect('login') 


def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


def upload_file(request):
    if request.method == 'POST':
        # Get the uploaded file
        uploaded_file = request.FILES.get('file')

        # Check if a file was uploaded
        if not uploaded_file:
            return render(request, 'upload.html', {'error': 'Please upload a file.'})

        # Process the uploaded file
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(uploaded_file)
        else:
            return render(request, 'upload.html', {'error': 'Unsupported file format. Please upload CSV or Excel files.'})

        # Save Inventories
        for column in df.columns[1:]:
            inventory_name = column.strip()  # Column names represent inventories
            Inventory.objects.get_or_create(name=inventory_name)

        # Save Products and their mapping to inventories
        for _, row in df.iterrows():
            product_name = str(row['Product']).strip()  # First column represents products
            product, _ = Product.objects.get_or_create(name=product_name)

            for column in df.columns[1:]:
                inventory_name = column.strip()
                inventory = Inventory.objects.get(name=inventory_name)

                # Check if the cell has data (not empty)
                if not pd.isna(row[column]):
                    mapping_name = f"{product_name}_{inventory_name}"
                    Products_in_inventories.objects.get_or_create(
                        name=mapping_name
                    )

        return render(request, 'home.html', {'message': 'Data saved successfully!'})

    return render(request, 'home.html')