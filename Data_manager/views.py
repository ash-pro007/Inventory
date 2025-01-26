from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
import pandas as pd
from .models import Inventory, Product, Products_in_inventories

# This varible will specify wheather user is admin or not 
is_user_admin = False

# Function to show login page
def login_page(request):
    return render(request, 'auth/login.html')

# Function to show signup page
def signup(request):
    return render(request, 'auth/signup.html')

# Function to show home page
def home(request):
    return HttpResponse("Hello World Django")


# Function to create new user
def register_user(request):
    if request.method == 'POST':
        # Getting all user details
        username = request.POST.get('username')
    
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # verifying details 
        if not username or not password1 or not password2:
            messages.error(request, 'All fields are required.')
            return render(request, 'signup.html')

        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'signup.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'signup.html')
        
        # Creating new user
        user = User.objects.create(
            username=username,
            password=make_password(password1) 
        )
        user.save()

        messages.success(request, 'Your account has been created successfully!')
        return redirect('login') 

    messages.success(request, 'Error! Couldn\'t create your account, please try again.')
    return render(request, 'signup.html')


# Login function 
def login_user(request):
    if request.method == 'POST':
        # Getting user detail for login
        username = request.POST['username']
        password = request.POST['password']

        # authenticating user from database
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
         
            return redirect('home') 
        else:
            messages.error(request, 'Invalid username or password.')
            return login_page(request)

    return login_page(request)


# Function to render home page
def home(request):
    global is_user_admin

    if request.user.is_authenticated:
        is_user_admin = request.user.is_superuser

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
                inv_dict[inven] = sorted(inv_dict[inven], key=lambda x: int(x[7:]))

     
        return render(request, 'home.html', {'is_user_admin': is_user_admin, 'inventories': inventories, 'inv_dict': inv_dict.items()})
    else:
        return redirect('login') 
    

# Logout Function
def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


# Function to upload data via csv/excel file
def upload_file(request):
    if request.method == 'POST':
    
        uploaded_file = request.FILES.get('file')

        # Checking wheather file is uploaded
        if not uploaded_file:
            messages.success(request, 'Please upload a file.')
            return home(request)

        # Identifying file format
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(uploaded_file)
        else:
            messages.success(request, 'Unsupported file format. Please upload CSV or Excel files.')
            return home(request)

        # Save Inventories
        for column in df.columns[1:]:
            inventory_name = column.strip() 
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


# Search individual product 
def search_product(request):
    if request.method == 'POST':
        # Getting product name to search
        product = request.POST['product']
        
        # Removing any extra spaces 
        product = product.strip().lower()

        # fetching all the products with their respected inventories
        products_in_inven = Products_in_inventories.objects.all()

        # list of inventories in which search product is present 
        inventory_lst = []

        for i in products_in_inven:
            val = i.name
            val = val.split('_')
            # compairng searched product string and searched product in inventory
            # if searched product is found in inventory then that inventory is add to the  inventory_lst
            if val[0].lower() == product:
                inventory_lst.append(val[1])

    inventory_lst = sorted(inventory_lst, key=lambda x: int(x.split()[1]))
        # returning the results
    return render(request, 'home.html', {'is_user_admin': is_user_admin, 'inventories': [], 'inv_dict': {}, 'inventory_lst': inventory_lst, 'searched_product': product.capitalize() })


# Function to search product by quantity/availability
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
                prod_dict[prod] = sorted(prod_dict[prod], key=lambda x: int(x.split()[1]))

    return render(request, 'home.html', {'is_user_admin': is_user_admin, 'inventories': [], 'inv_dict': {}, 'prod_dict': prod_dict.items()})


## Extra functionalities 


# Function to add a new inventory 
def add_inventory(request):
    if request.method == 'POST':
        
        inventory_to_add = request.POST['inventory-to-add'].strip()  # getting new inventory name

        if Inventory.objects.filter(name=inventory_to_add).exists(): # checking if that inventory name already exists
            messages.error(request, f'{inventory_to_add}  already exists!')
        else:
            new_inventory = Inventory(name=inventory_to_add) # making object of Inventory model
            new_inventory.save()                             # saving that object in db
            messages.success(request, f'{inventory_to_add}  added successfully!')
    
    return home(request)


# Function to add a new product
def add_product(request):
    if request.method == 'POST':
        product_to_add = request.POST['product-to-add'].strip()  # getting new product name

        if Product.objects.filter(name=product_to_add).exists():
            messages.error(request, f'{product_to_add}  already exists!') # checking if that product name already exists
        else:
            new_inventory = Product(name=product_to_add)  # making object of Product model
            new_inventory.save()                          # saving that object in db
            messages.success(request, f'{product_to_add}  added successfully!') 
    
    return home(request)


# Function to add a existing product in an existing inventory
def add_product_in_inventory(request):
    if request.method == 'POST':
        product = request.POST['product-chk'].strip()  # getting product name
        inventory = request.POST['inventory-ch'].strip() # getting product name

        if not Product.objects.filter(name=product).exists(): # making sure that the given product already exists to put in inventory
            messages.error(request, f'{product}  doesn\'t exist! Please add {product} first.')
            return home(request)
        
        if not Inventory.objects.filter(name=inventory).exists(): # making sure that the given inventory already exists
            messages.error(request, f'{inventory}  doesn\'t exist! Please add {inventory} first.')
            return home(request)

        product_in_inventory = product + '_' + inventory  # create a new string in format 'Product_Inventory' to save in db

        if Products_in_inventories.objects.filter(name=product_in_inventory).exists(): # again checking wheather that new format string already exists
            messages.error(request, f'{product}  already exists in {inventory} .')
            return home(request)


        new_product_in_inventory = Products_in_inventories(name=product_in_inventory) # makeing model object
        new_product_in_inventory.save()                                               # saving that object in db

        messages.success(request, f'{product} has been succussfully added in {inventory}.')

    return home(request)


def reset_database(request):
    try:
        # Delete all data from each model
        Inventory.objects.all().delete()
        Product.objects.all().delete()
        Products_in_inventories.objects.all().delete()

        messages.success(request, 'Inventory has been successfully reset')
    except Exception as e:
        print(f"An error occurred while deleting data: {e}")
    return home(request)
  