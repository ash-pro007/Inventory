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

is_user_admin = False

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


def logout_user(request):
    logout(request)
    return redirect('login')

def home(request):
    global is_user_admin

    if request.user.is_authenticated:
        is_user_admin = request.user.is_superuser
        
        # 

        # inv_dict = {}

        # inventories = Inventory.objects.all()

        # for i in inventories:
        #     inv_dict.update({i.name: []})

        # print(inv_dict)

        # products_in_inven = Products_in_inventories.objects.all()

        # for i in products_in_inven:

        #     pin = i.name

        #     lst = pin.split('_')
        #     prod = lst[0]
        #     inven = lst[1]

        #     tem_prod_lst = inv_dict.get(inven)

        #     tem_prod_lst.append(prod)

        #     inv_dict.update({inven: tem_prod_lst})

        inv_dict = {}

        # Initialize the dictionary with inventory names as keys and empty lists as values
        inventories = Inventory.objects.all()
        for inventory in inventories:
            inv_dict[inventory.name] = []

        # Fetch all Products_in_inventories records
        products_in_inven = Products_in_inventories.objects.all()

        # Process each record and update the dictionary
        for record in products_in_inven:
            # Extract product and inventory names
            pin = record.name
            prod, inven = pin.split('_')  # Assuming the format is always 'Product_Inventory'

            # Append the product to the appropriate inventory's list
            if inven in inv_dict:
                inv_dict[inven].append(prod)

        # Debugging - Print the resulting dictionary
        # print("\n\n\n")
        # print(inv_dict)
        # print("\n\n\n")


        # print("\n\n\nThe dictionary after::::::::: ", inv_dict, "\n\n\n\n")
     
        return render(request, 'home.html', {'is_user_admin': is_user_admin, 'inventories': inventories, 'inv_dict': inv_dict.items()})
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
            messages.success(request, 'Please upload a file.')
            return home(request)

        # Process the uploaded file
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(uploaded_file)
        else:
            messages.success(request, 'Unsupported file format. Please upload CSV or Excel files.')
            return home(request)

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

        messages.success(request, 'Data saved successfully!')
        return home(request)
        # return render(request, 'home.html', {'message': 'Data saved successfully!'})

    return home(request)


def search_product(request):
    if request.method == 'POST':
        product = request.POST['product']

        product = product.strip().lower()

        products_in_inven = Products_in_inventories.objects.all()

        inventory_lst = []

        for i in products_in_inven:
            val = i.name
            
            val = val.split('_')
     
            if val[0].lower() == product:
                inventory_lst.append(val[1])

        print('\n\n invetnroy lst ------------>  ', inventory_lst)

    return render(request, 'home.html', {'is_user_admin': is_user_admin, 'inventories': [], 'inv_dict': {}, 'inventory_lst': inventory_lst, 'searched_product': product.capitalize() })


def search_by_quantity(request):
    if request.method == 'POST':
        quantity = request.POST['quantity'].strip()

        quantity = int(quantity)

        prod_dict = {}

        all_products = Product.objects.all()
        products_in_inven = Products_in_inventories.objects.all()
        
        for product in all_products:
            prod_dict[product.name] = []


        for record in products_in_inven:
            # Extract product and inventory names
            pin = record.name
            prod, inven = pin.split('_')  # Assuming the format is always 'Product_Inventory'

            # Append the product to the appropriate inventory's list
            if prod in prod_dict:
                prod_dict[prod].append(inven)
        
     

        # Extacting the products which are avaiable in equal or more inventories 
        # putting them in a new list

        new_list = []

        for key, value in prod_dict.items():
            if len(value) >= quantity:
                new_list.append(key)

        # clearling prod_dict to make product as key where list of inventory in equal or more
        
        prod_dict.clear()

        for product in new_list:
            prod_dict[product] = []

        
        for record in products_in_inven:
            # Extract product and inventory names
            pin = record.name
            prod, inven = pin.split('_')  # Assuming the format is always 'Product_Inventory'

            # Append the product to the appropriate inventory's list
            if prod in prod_dict:
                prod_dict[prod].append(inven)

    return render(request, 'home.html', {'is_user_admin': is_user_admin, 'inventories': [], 'inv_dict': {}, 'prod_dict': prod_dict.items()})