from django.shortcuts import render,redirect
from django.http import JsonResponse
import requests
from rest_framework.response import Response
from django.contrib import messages
from rest_framework import status
import json
from admin_dashboard.views import products_related_base_url
user_base_url='https://users-1wfh.onrender.com/api/'  #base url for the users backend api
# Create your views here.

# User Module----------------
def get_access_token(request):      #to get access token for the user from cookie.
    return request.COOKIES.get('access_token')

def refresh_access_token(request):         #refresh access token ....
    refresh_token=request.COOKIES.get('refresh_token')
    if not refresh_token:
        return None
    url=user_base_url+'refresh/'
    try:
        response=requests.post(url,data={
            "refresh":refresh_token
        })
        if response.status_code==200:
            data=response.json()
            return data.get('access')
        else:
            return None
    except request.exceptions.RequestException:
        return None

def get_all_product_images(request):
    image_url = products_related_base_url + 'product-images/'  # new API endpoint
    images = []
    if request.method == 'GET':
        try:
            response = requests.get(url=image_url)
            response.raise_for_status()
            images = response.json()
        except requests.exceptions.RequestException as e:
            messages.error(request, f"Failed to fetch product images: {str(e)}")
        except ValueError as e:
            messages.error(request, f"Invalid response format for images: {str(e)}")
    return images

def check_is_authentictated(request):
    is_authenticated = False
    access_token = get_access_token(request)
    if not access_token:
        new_token = refresh_access_token(request)
        if new_token:
            is_authenticated = True
        else:
            is_authenticated = False
    else:
        is_authenticated = True   
    return JsonResponse({"message":"success","is_authenticated":is_authenticated},status=status.HTTP_200_OK)


def index(request):
    resp= check_is_authentictated(request)
    if resp.status_code==200:
        data = json.loads(resp.content.decode("utf-8"))
        is_authenticated=(data["is_authenticated"])
    else:
        is_authenticated=False
    # Fetch all products
    product_url = products_related_base_url + 'products/'
    products = []
    try:
        response = requests.get(url=product_url)
        response.raise_for_status()
        products = response.json()
    except requests.exceptions.RequestException as e:
        messages.error(request, f"Failed to fetch products: {str(e)}")
    except ValueError as e:
        messages.error(request, f"Invalid response format for products: {str(e)}")

    # Combine all info in context
    context = {
        "is_authenticated": is_authenticated,
        "products": products,
    }

    return render(request, 'index.html', context)  #index html page 

def home(request):
    return render(request,'home.html')    #home html page

def login(request):                         #for login html page with error handling
    if request.method=='GET':
        return render(request,'login.html')

def set_cookie(request,data,redirect_url):    #to set cookies(access_tokn,refresh_token,user_id,username)
    resp=redirect(redirect_url)
    #setting cookies
    resp.set_cookie(
        "access_token",
        data['access_token'],
        max_age=20 * 60,# 20 minutes in seconds
        httponly=True,
        secure=False,
        samesite='lax'
    )
    resp.set_cookie(
        "refresh_token",
        data['refresh_token'],
        max_age= 7 * 24 * 60 * 60,
        httponly=True,
        secure=False,
        samesite='lax'
    )
    resp.set_cookie(
        "user_id",
        data['user_id'],
        max_age= 7 * 24 * 60 * 60,
    )
    resp.set_cookie(
        "username",
        data["user_name"],
        max_age=7 * 24 * 60 * 60,
    )
    return resp

def if_not_new_token(request):     #if_not_new_token
    resp= redirect('/')
    for key in request.COOKIES.keys():
        resp.delete_cookie(key)
    return resp
    
def profile(request):                          # profile html page 
    if request.method=='GET':
        access_token=get_access_token(request)
        if not access_token:
            new_token=refresh_access_token(request)
            if not new_token:
                return if_not_new_token(request)
            access_token=new_token
        headers={
            "Authorization":f"Bearer {access_token}"
        }
        url=user_base_url+'account'
        profile_data={}
        try:
            response=requests.get(url=url,headers=headers)
            data=response.json()
            if response.status_code==200:
                
                profile_data.update({"email":data['email']})
                profile_data.update({"username":data['username']})
                profile_data.update({"name":data['name']})
                profile_data.update({"role":data['role']})
                profile_data.update({"address":data['address']})
                profile_data.update({"mobile_number":data['mobile_number']})
                profile_data.update({"profile_pic":data['profile_pic']})
                profile_data.update({"is_active":data['is_active']})
            
            resp= render(request,'profile.html',{"profile":profile_data})
            access_token_expiry = 20 * 60  # 20 minutes in seconds
                #setting cookies
            resp.set_cookie(
                    "access_token",
                    access_token,
                    max_age=access_token_expiry,
                    httponly=True,
                    secure=False,
                    samesite='lax'
                )
            
            return resp

        except requests.exceptions.RequestException as e:
            messages.error(request, str(e))
            return redirect('/')
    # return redirect('/profile')

def verify_login(request):                      #to verify user credentials and setting cookies.
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        # print(f"username{username} and password {password}")
        url=user_base_url+'login'
        try:
            response=requests.post(url=url,data={
                "username":username,
                "password":password
            })
            data=response.json()

            if "access_token" in data and "refresh_token" in data:
                #prepared json response
                redirect_url='/'
                resp=set_cookie(request,data,redirect_url)
                return resp
            else:
                # Invalid credentials → redirect back to login page
                messages.error(request,f"Invalid credentials", extra_tags='login')
                return redirect('/')
        except requests.exceptions.RequestException as e:
            messages.error(request,f"{str(e)}", extra_tags='login')
            return redirect('/')
                   
def logout(request):                 #to logout the user.
    if request.method=='GET':
        access_token=get_access_token(request)
        if not access_token:
            new_token=refresh_access_token(request)
            if not new_token:
                return if_not_new_token(request)
            access_token=new_token
        headers={
                "Authorization":f"Bearer {access_token}"
        }
        url=user_base_url+'logout'
        try:
            response=requests.post(url=url,headers=headers)
            data=response.json()
            return if_not_new_token(request)
        except:
            pass

def register(request):                      #to load register html
    if request.method=='GET':
        return render(request,'register.html')

def verify_register(request):        #to verify register
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Use JSON format for the POST request to the external API
        url = user_base_url + 'register'
        try:
            response = requests.post(url=url, json={
                "username": username,
                "email": email,
                "password": password
            })

            if response.status_code==201:
                messages.error(request,"Registration is complete you can now login",extra_tags='goto_success')
                return redirect('/?auth=login')
            else:
                errors=response.json()
                for message in errors.values():
                    messages.error(request,f"{message}",extra_tags='register')
                return redirect('/')


        except requests.exceptions.RequestException as e:
            messages.error(request,f"{str(e)}",extra_tags='register')
            return redirect('/')

def profile_update(request):            #to update the profile of the user.
    if request.method=='POST':
        print(f'in-post')
        access_token=get_access_token(request)
        if not access_token:
            new_token=refresh_access_token(request)
            if not new_token:
                return if_not_new_token(request)
            access_token=new_token
        name=request.POST.get('name')
        mobile_number=request.POST.get('mobile_number')
        address=request.POST.get('address')
        headers={
            "Authorization":f"Bearer {access_token}"
        }
        url=user_base_url+'account'
        try:
            response=requests.put(url=url,headers=headers,json={
                "name":name,
                "mobile_number":mobile_number,
                "address":address
            })
            data=response.json()
            
            if response.status_code==200:
                messages.success(request,f"Succesfully update")
            else:
                messages.error(request,"Failed to update the profile")
        except requests.exceptions.RequestException as e:
            messages.error(request,f"{str(e)}")
        resp= redirect('/profile')
        access_token_expiry = 20 * 60  # 20 minutes in seconds
                #setting cookies
        resp.set_cookie(
                    "access_token",
                    access_token,
                    max_age=access_token_expiry,
                    httponly=True,
                    secure=False,
                    samesite='lax'
                )
            
        return resp

    # return redirect('/profile')
            
             
#User Module------------------



#products ----------------------

products_base_url='https://products-k4ov.onrender.com/api/'
def shop(request):       #to get shop all page provide all products data
    if request.method=='GET':
        resp=check_is_authentictated(request)
        if resp.status_code==200:
            data=json.loads(resp.content.decode("utf-8"))
            is_authenticated=(data["is_authenticated"])
        else:
            is_authenticated=False
        products=[]
        url=products_base_url+'products'
        try:
            response=requests.get(url=url)
            response.raise_for_status()
            products=response.json()
        except requests.exceptions.RequestException as e:
            messages.error(request,f"failed to fetch {str(e)}")
        return render(request,'shop.html',{"products":products,"is_authenticated": is_authenticated})


def product_detail(request,slug):       # product deatil page using slug 
    resp=check_is_authentictated(request)
    if resp.status_code==200:
        data=json.loads(resp.content.decode("utf-8"))
        is_authenticated=(data["is_authenticated"])
    else:
        is_authenticated=False
    product_detail_url=products_base_url+f"products/{slug}"
    product=[]
    try:
        response=requests.post(url=product_detail_url)
        response.raise_for_status()
        product=response.json()
    except requests.exceptions.RequestException as e:
        messages.error(request,f"failed to fetch product detail : {str(e)}")
    return render(request,'product-detail.html',{"product":product,"is_authenticated": is_authenticated})


def category_wise_products(request, slug):      # category wise products data
    resp=check_is_authentictated(request)
    if resp.status_code==200:
        data=json.loads(resp.content.decode("utf-8"))
        is_authenticated=(data["is_authenticated"])
    else:
        is_authenticated=False
    products_detail_url = products_base_url + "products/"
    products = []

    try:
        # ✅ MUST BE GET
        response = requests.get(products_detail_url)
        response.raise_for_status()

        all_products = response.json()

        # ✅ Filter by category slug
        products = [
            product for product in all_products
            if product.get("category", {}).get("slug") == slug
        ]

        print("CATEGORY SLUG:", slug)
        # print("FILTERED PRODUCTS:", products)

    except requests.exceptions.RequestException as e:
        messages.error(request, f"failed to fetch product detail : {str(e)}")

    return render(request,"shop.html",{"products": products,"category_name": slug,"is_authenticated": is_authenticated,})

cart_url="http://127.0.0.1:8002/api/cart/"

def add_to_cart(request):       # add to cart functionalities
    if request.method=='POST':
        print('in post')
        access_token=get_access_token(request)
        if not access_token:
            new_token=refresh_access_token(request)
            if not new_token:
                return if_not_new_token(request)
            access_token=new_token
        print(access_token)
        headers={
            "Authorization": f"Bearer {access_token}"
        }
        url=f"{cart_url}add/"
        try:
            print('in try')
            response=requests.post(url=url,headers=headers,json={"variant_id": request.POST.get("variant_id"),"product_slug": request.POST.get("product_slug"),"quantity": 1,})
            response.raise_for_status()
            print(f"response{response.json()}")
        except requests.exceptions.RequestException as e:
            messages.error(request,f"failed to add to cart : {str(e)}")
        return redirect('/')
    

def get_cart_details(request):     # to get cart details
    if request.method=='GET':
        access_token=get_access_token(request)
        if not access_token:
            new_token=refresh_access_token(request)
            if not new_token:
                return if_not_new_token(request)
            access_token=new_token
        cart_data=[]
        try:
            cart_resp=requests.get(url=cart_url,headers={"Authorization": f"Bearer {access_token}"})
            print(cart_resp.json())
            cart_resp.raise_for_status()
            cart_data = cart_resp.json()
        except requests.exceptions.RequestException as e:
            messages.error(request,f"failed to add to cart : {str(e)}")
        print(f"cart data\n{cart_data}")
        resp=render(request,"cart.html",{"cart": cart_data,'is_authenticated':True})
        access_token_expiry = 20 * 60  # 20 minutes in seconds
                #setting cookies
        resp.set_cookie(
                    "access_token",
                    access_token,
                    max_age=access_token_expiry,
                    httponly=True,
                    secure=False,
                    samesite='lax'
                )
        return resp 


def delete_cart_item(request):     # to delete cart item 
    if request.method=='POST':
        access_token=get_access_token(request)
        if not access_token:
            new_token=refresh_access_token(request)
            if not new_token:
                return if_not_new_token(request)
            access_token=new_token
        

        item_id=int(request.POST.get('id'))
        headers={
            "Authorization": f"Bearer {access_token}"
        }
        cart_item_delete_url=f"{cart_url}item/{item_id}/delete/"
        try:
            response=requests.delete(url=cart_item_delete_url,headers=headers)
            response.raise_for_status()
            # print(f"update cart response : {response}")
        except requests.exceptions.RequestException as e:
            messages.error(request,f"failed to delete cart item : {str(e)}")
        resp=redirect('/cart')
        access_token_expiry = 20 * 60  # 20 minutes in seconds
                #setting cookies
        resp.set_cookie(
                    "access_token",
                    access_token,
                    max_age=access_token_expiry,
                    httponly=True,
                    secure=False,
                    samesite='lax'
                )
        return resp 



def update_cart_item(request):    # to update cart items functionalites
    if request.method=='POST':
        access_token=get_access_token(request)
        if not access_token:
            new_token=refresh_access_token(request)
            if not new_token:
                return if_not_new_token(request)
            access_token=new_token
        

        item_id=int(request.POST.get('id'))
        item_quantity=int(request.POST.get('quantity'))
        item_operation=int(request.POST.get('operation'))
        if item_operation==0:
            item_quantity-=1
        else:
            item_quantity+=1
        
        headers={
            "Authorization": f"Bearer {access_token}"
        }
        if item_quantity>0:
            payload={
                'quantity':item_quantity
            }
            cart_update_url=f"{cart_url}item/{item_id}/update/"
            try:
                response=requests.patch(url=cart_update_url,headers=headers,json=payload)
                response.raise_for_status()
                # print(f"update cart response : {response}")
            except requests.exceptions.RequestException as e:
                messages.error(request,f"failed to update cart item : {str(e)}")
            return redirect('/cart')
        else:
            resp= delete_cart_item(request)
            access_token_expiry = 20 * 60  # 20 minutes in seconds
                #setting cookies
        resp.set_cookie(
                    "access_token",
                    access_token,
                    max_age=access_token_expiry,
                    httponly=True,
                    secure=False,
                    samesite='lax'
                )
        return resp 

checkout_url="http://127.0.0.1:8002/api/checkout/"

def checkout(request):
        access_token=get_access_token(request)
        if not access_token:
            new_token=refresh_access_token(request)
            if not new_token:
                return if_not_new_token(request)
            access_token=new_token
        

        headers={
            "Authorization":f"Bearer {access_token}"
        }
        url=checkout_url
        context={}
        try:
            response=requests.post(url=url,headers=headers)
            response.raise_for_status()
            checkout_data=response.json()
            context = {
            "checkout_data": [checkout_data]  # wrap in list
            }
            print(f" the checkout data\n {checkout_data}")
        except requests.exceptions.RequestException as e:
            messages.error(request,f"failed during checkout : {str(e)}")
        return render(request,'temp.html',context)


order_url="http://127.0.0.1:8002/api/get-all-orders/"

def get_all_orders(request):
    if request.method=='GET':
        access_token=get_access_token(request)
        if not access_token:
            new_token=refresh_access_token(request)
            if not new_token:
                return if_not_new_token(request)
            access_token=new_token
        

        headers={
            "Authorization":f"Bearer {access_token}"
        }

        url=order_url
        context={}
        try:
            response=requests.get(url=url,headers=headers)
            response.raise_for_status()
            orders=response.json()
            context = {
            "orders": orders["orders"]  # wrap in list
            }
            print(f"the orders is \n {orders}")
        except requests.exceptions.RequestException as e:
            messages.error(request,f"failed to fetch orders : {str(e)}")
        return render(request,'temp2.html',context)

                    