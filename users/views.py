from django.shortcuts import render,redirect
from django.http import JsonResponse
import requests
from rest_framework.response import Response
from django.contrib import messages

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
    
def index(request):
    if request.method=='GET':
        is_authenticate = False
        access_token=get_access_token(request)
        if not access_token:
            new_token=refresh_access_token(request)
            if new_token:
                is_authenticate = True
            else:
                is_authenticate = False
        else:
            is_authenticate=True

        return render(request,'index.html',{"is_authenticated":is_authenticate})  #index html page 

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
        try:
            response=requests.get(url=url,headers=headers)
            data=response.json()
            if response.status_code==200:
                profile_data={}
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
        return redirect('/profile')
    # return redirect('/profile')
            
             
#User Module------------------



#products ----------------------

products_base_url='https://products-k4ov.onrender.com/api/'
def shop(request):
    if request.method=='GET':
        products_data=[]
        url=products_base_url+'products'
        try:
            response=requests.get(url=url)
            data=response.json()
            if response.status_code==200:
                products_data=data
                print(products_data)
                return render(request,'shop.html',{'products': products_data})
            else:
                messages.error(request,"products not available")
                return render(request,'shop.html')
        except requests.exceptions.RequestException as e:
            messages.error(request,f"{str(e)}")
            return render(request,'shop.html')

                

                