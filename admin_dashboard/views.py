from django.shortcuts import render,redirect
from django.http import JsonResponse
import requests
from rest_framework.response import Response
from django.contrib import messages
# Create your views here.

#imports of some comman methods that are written in users.views
admin_base_url='https://admin-9opv.onrender.com/api/admin/'

#admin releated views

def admin_refresh_access_token(request):         # admin refresh access token ....
    refresh_token=request.COOKIES.get('refresh_token')
    if not refresh_token:
        return None
    url=admin_base_url+'refresh/'
    try:
        response=requests.post(url,data={
            "refresh":refresh_token
        })
        if response.status_code==200:
            data=response.json()
            return data.get('access')
        else:
            return None
    except requests.exceptions.RequestException:
        return None

def admin_get_access_token(request):      # admin to get access token for the user from cookie.
    return request.COOKIES.get('access_token')

def admin_if_not_new_token(request):     # admin if_not_new_token
    resp= redirect('/admin/login?token=expired')
    for key in request.COOKIES.keys():
        resp.delete_cookie(key)
    return resp

def admin_profile(request):                          # profile html page 
    if request.method=='GET':
        access_token=admin_get_access_token(request)
        if not access_token:
            new_token=admin_refresh_access_token(request)
            if not new_token:
                return admin_if_not_new_token(request)
            access_token=new_token
        headers={
            "Authorization":f"Bearer {access_token}"
        }
        url=admin_base_url+'profile/'    
          
        try:
            
            response=requests.get(url=url,headers=headers)
            data=response.json()
            if response.status_code==200:
                admin_profile_data={}
                admin_profile_data.update({"email":data['email']})
                admin_profile_data.update({"username":data['username']})
                admin_profile_data.update({"name":data['name']})
                admin_profile_data.update({"mobile_number":data['mobile_number']})
                admin_profile_data.update({"profile_pic":data['profile_pic']})
                
            
                resp= render(request,'admin_index.html',{"profile":admin_profile_data})
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
            else:
                resp= render(request,'admin_index.html')
            return resp

        except requests.exceptions.RequestException as e:
            messages.error(request, str(e))
            return redirect('/admin/login?tokenr=error')
        
def admin_index(request):         #admin index page
    return admin_profile(request)    

def admin_login(request):         #admin login page
    token_status=request.GET.get('token')
    if token_status=='expired' or token_status=='error':
        return render(request,'admin_login.html')
    else:
         return admin_profile(request)


def admin_set_cookie(request,data,redirect_url):    #to set admin cookies(access_tokn,refresh_token)
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
    # resp.set_cookie(
    #     "user_id",
    #     data['user_id'],
    #     max_age= 7 * 24 * 60 * 60,
    # )
    # resp.set_cookie(
    #     "username",
    #     data["user_name"],
    #     max_age=7 * 24 * 60 * 60,
    # )
    return resp

def admin_verify_login(request):    #admin verify login
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        # print(f"username{username} and password {password}")
        url=admin_base_url+'login/'
        try:
            response=requests.post(url=url,data={
                "username":username,
                "password":password
            })
            data=response.json()
            print(data)

            if "access_token" in data and "refresh_token" in data:
                #prepared json response
                redirect_url='/admin/'
                resp=admin_set_cookie(request,data,redirect_url)
                return resp
            else:
                # Invalid credentials → redirect back to login page
                messages.error(request,f"Invalid credentials", extra_tags='admin_login')
                return redirect('/admin/login/')
        except requests.exceptions.RequestException as e:
            messages.error(request,f"{str(e)}", extra_tags='admin_login')
            return redirect('/admin/login/')
        

def admin_logout(request):
    if request.method=='GET':
        access_token=admin_get_access_token(request)
        if not access_token:
            new_token=admin_refresh_access_token(request)
            if not new_token:
                return admin_if_not_new_token(request)
            access_token=new_token
        headers={
                "Authorization":f"Bearer {access_token}"
        }
        url=admin_base_url+'logout/'
        try:
            response=requests.post(url=url,headers=headers)
            data=response.json()
            return admin_if_not_new_token(request)
        except:
            pass


products_related_base_url='https://products-k4ov.onrender.com/api/'

#category related views

def add_category(request):                 #to add categories and get categories....
    category_url=products_related_base_url+'categories/'
    if request.method=='GET':
        url=category_url
        categories=[]
        try:
            response=requests.get(url=url)
            response.raise_for_status()
            categories=response.json()
            # print(categories)
        except requests.exceptions.RequestException as e:
            messages.error(request,f"failed to fetch categories data :{str(e)}")
        except ValueError as e:
            messages.error(request, f"Invalid response format: {str(e)}")
        return render(request,'add_category.html',{"categories":categories})
        
    if request.method=='POST':
        category_name=request.POST.get('category_name')
        url=category_url
        try:
            response=requests.post(url=url,json={
                "category_name":category_name
            })
            data=response.json()
            if response.status_code in [200,201]:
                messages.success(request,"category added successfully")
            else:
                messages.error(request,"category not added")
            return redirect('/admin/add-category')
        except requests.exceptions.RequestException as e:
            messages.error(request,f"{str(e)}")
        return redirect('/admin/add-category')
    

def edit_category(request,category_id):        # to edit category
    edit_category_url=f"{products_related_base_url}categories/{category_id}/"
    if request.method=='GET':
        category_data={}
        try:
            response=requests.get(url=edit_category_url)
            response.raise_for_status()
            category_data=response.json()
        except requests.exceptions.RequestException as e:
            messages.error(request,f"failed to fetch the data",{str(e)})
            return render(request,'add_category.html')
        return render(request,'edit_category.html',{"category":category_data})
    
    if request.method=='POST':
        category_name=request.POST.get('category_name')
        try:
            response=requests.put(url=edit_category_url,json={
                "category_name":category_name
            })
            response.raise_for_status()
            messages.success(request,"Category edited successfully")
        except requests.exceptions.RequestException as e:
            messages.error(request,f"failed to update category : {str(e)}")
        return redirect('/admin/add-category')
    
def delete_category(request,category_id):
    delete_category_url=f"{products_related_base_url}categories/{category_id}/"
    if request.method=='GET':
        try:
            response=requests.delete(url=delete_category_url)
            response.raise_for_status()
            messages.success(request,"Deleted Sucessfully")
        except requests.exceptions.RequestException as e:
            messages.error(request,f"unable to delete : str{(e)}")
        return render(request,'add_category.html')








