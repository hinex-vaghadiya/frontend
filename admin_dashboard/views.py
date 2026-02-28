from django.shortcuts import render,redirect
from django.http import JsonResponse
import requests
from rest_framework.response import Response
from django.contrib import messages
from rest_framework import status
import json
import os
user_base_url="https://users-1wfh.onrender.com/api/"
# Create your views here.

#imports of some comman methods that are written in users.views
admin_base_url='https://admin-9opv.onrender.com/api/admin/'

#admin releated views

def admin_refresh_access_token(request):         # admin refresh access token ....
    refresh_token=request.COOKIES.get('admin_refresh_token')
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
    return request.COOKIES.get('admin_access_token')

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
                        "admin_access_token",
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
    # return admin_profile(request) 
    return customer_data(request)

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
        "admin_access_token",
        data['access_token'],
        max_age=20 * 60,# 20 minutes in seconds
        httponly=True,
        secure=False,
        samesite='lax'
    )
    resp.set_cookie(
        "admin_refresh_token",
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

#-------all product related------------------
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
    

def edit_category(request,slug):        # to edit category
    edit_category_url=f"{products_related_base_url}categories/{slug}/"
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
    
def delete_category(request,slug):       # to delete category
    delete_category_url=f"{products_related_base_url}categories/{slug}/"
    if request.method=='GET':
        try:
            response=requests.delete(url=delete_category_url)
            response.raise_for_status()
            messages.success(request,"Deleted Sucessfully")
        except requests.exceptions.RequestException as e:
            messages.error(request,f"unable to delete : str{(e)}")
        return redirect('/admin/add-category')


#products related views

def get_all_categories(request):  # to get all caregories  details for add product
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
        return render(request,'add_product.html',{"categories":categories})
    

def get_all_products(request,destination):         # to get all products  details for add variant
    product_url=products_related_base_url+'products/'
    if request.method=='GET':
        url=product_url
        products=[]
        try:
            response=requests.get(url=url)
            response.raise_for_status()
            products=response.json()
            # print(categories)
        except requests.exceptions.RequestException as e:
            messages.error(request,f"failed to fetch products data :{str(e)}")
        except ValueError as e:
            messages.error(request, f"Invalid response format: {str(e)}")
        return render(request,destination,{"products":products})


def get_all_variants(request):         # to get all products  details for add variant
    variant_url=products_related_base_url+'variants/'
    if request.method=='GET':
        url=variant_url
        variants=[]
        try:
            response=requests.get(url=url)
            response.raise_for_status()
            variants=response.json()
            # print(categories)
        except requests.exceptions.RequestException as e:
            messages.error(request,f"failed to fetch variants data :{str(e)}")
        except ValueError as e:
            messages.error(request, f"Invalid response format: {str(e)}")
        return render(request,'add_batch.html',{"variants":variants})


#no bugs regarding render and redirect...

def product_list(request):  # to serve the product list page 
    return get_all_products(request,'product_list.html')


def add_product_and_images(request):                   # to add product and images
    if request.method=='POST':
        product_url=products_related_base_url+'products/'
        product_images_url=products_related_base_url+'product-images/'

        is_active=True
        images =request.FILES.getlist('product_images')
        primary_index=int(request.POST.get('primary_image_index'))
        payload={
            "product_name":request.POST.get('product_name'),
            "description":request.POST.get('description'),
            "is_active":is_active,
            "category_id":int(request.POST.get('category_id'))
        }
        try:
            product_response=requests.post(url=product_url,data=payload)
            product_response.raise_for_status()
            product_data=product_response.json()
            product_id=int(product_data['product_id'])
            for idx,img in enumerate(images):
                is_primary=(idx==primary_index)
                files = {
                'image': (img.name, img, img.content_type)
            }   
                payload = {
                'product': product_id,
                'is_primary': is_primary  # API may expect string "true"/"false"
            }
                try:
                    image_response=requests.post(url=product_images_url,files=files,data=payload)
                    print(image_response.json())
                    image_response.raise_for_status()
                    print(f"Image {img.name} uploaded successfully")
                except requests.exceptions.RequestException as e:
                    return JsonResponse({"error":f"Unable to upload image {img.name}: {str(e)}"})
            return JsonResponse({"message":"success","product_id":product_id},status=status.HTTP_200_OK)
        except requests.exceptions.RequestException as e:
            return JsonResponse({"error":f"unable to add product : {str(e)}"})  
        
def extract_variant_indexes(request):   #to extract indexes of multiple variants or handle multiple variants
    indexes = set()
    for key in request.POST.keys():
        if key.startswith("variants["):
            idx = key.split("[")[1].split("]")[0]
            indexes.add(idx)
    
    sorted_indexes = sorted(indexes, key=int)  # numeric sort
    print("DEBUG: Extracted variant indexes:", sorted_indexes)  # debug print
    return sorted_indexes
    

def add_variant_and_images(request, product_id):  # to add variant and images
    if request.method == 'POST':
        # print('i am in variant')

        variant_url = products_related_base_url + 'variants/'
        variant_images_url = products_related_base_url + 'variant-images/'

        variant_indexes = extract_variant_indexes(request)
        print("Variant indexes:", variant_indexes)

        try:
            for idx in variant_indexes:
                payload = {
                    "product": int(product_id),
                    "name": request.POST.get(f"variants[{idx}][name]"),
                    "price": int(request.POST.get(f"variants[{idx}][price]")),
                    "stock": 0,
                    "compare_at_price": int(request.POST.get(f"variants[{idx}][compare_at_price]")),
                }

                print(f"Variant payload {idx}:", payload)

                variant_response = requests.post(url=variant_url, data=payload)
                variant_response.raise_for_status()
                variant_data = variant_response.json()
                print(variant_data)

                variant_id = int(variant_data['id'])

                images = request.FILES.getlist(f"variants[{idx}][images]")
                print(f"Variant {idx} images:", images)

                for img in images:
                    files = {
                        'image': (img.name, img, img.content_type)
                    }
                    image_payload = {
                        'variant': variant_id
                    }

                    variant_image_response = requests.post(
                        url=variant_images_url,
                        files=files,
                        data=image_payload
                    )

                    print(variant_image_response.json())
                    variant_image_response.raise_for_status()
                    print(f"Image {img.name} uploaded successfully")

            messages.success(request, "Product with mentioned variants added successfully")
            return redirect('/admin/product-list')

        except requests.exceptions.RequestException as e:
            messages.error(request, f"unable to add variant : {str(e)}")
            return redirect('/admin/product-list/')


def add_product(request):               # to add product along with its variants
    if request.method=='GET':     
        return get_all_categories(request)
    
    if request.method=='POST':
        resp= add_product_and_images(request)
        if resp.status_code==200:
            data = json.loads(resp.content.decode("utf-8"))
            product_id=(data["product_id"])
            return add_variant_and_images(request,product_id)
            
        else:
            data = json.loads(resp.content.decode("utf-8"))
            messages.error(request,data["error"])
            return redirect('/admin/product-list')

def edit_product(request, slug):
    product_detail_url = products_related_base_url + f"products/{slug}/"
    category_url = products_related_base_url + 'categories/'
    
    if request.method == 'GET':
        product = {}
        categories = []
        try:
            # Fetch categories
            cat_response = requests.get(url=category_url)
            cat_response.raise_for_status()
            categories = cat_response.json()
            
            # Fetch product details (using exact mechanism from users/views.py)
            response = requests.post(url=products_related_base_url + f"products/{slug}")
            response.raise_for_status()
            product = response.json()
        except requests.exceptions.RequestException as e:
            messages.error(request, f"Failed to fetch product detail: {str(e)}")
            return redirect('/admin/product-list')
            
        return render(request, 'edit_product.html', {"product": product, "categories": categories})
        
    if request.method == 'POST':
        is_active = request.POST.get('is_active') == 'on'
        payload = {
            "product_name": request.POST.get('product_name'),
            "description": request.POST.get('description'),
            "is_active": is_active,
            "category_id": int(request.POST.get('category_id'))
        }
        product_id = request.POST.get('product_id')
        
        try:
            # Use PUT to update base product
            response = requests.put(url=product_detail_url, data=payload)
            response.raise_for_status()
            
            # Handle new images
            new_images = request.FILES.getlist('new_images')
            if new_images and product_id:
                product_images_url = products_related_base_url + 'product-images/'
                for img in new_images:
                    files = {'image': (img.name, img, img.content_type)}
                    payload_img = {'product': product_id, 'is_primary': 'false'} # Default explicitly false
                    img_response = requests.post(url=product_images_url, files=files, data=payload_img)
                    img_response.raise_for_status()
            
            messages.success(request, "Product updated successfully")
        except requests.exceptions.RequestException as e:
            messages.error(request, f"Failed to update product: {str(e)}")
            
        return redirect(f'/admin/edit-product/{slug}')

def delete_product_image(request, image_id, slug):
    url = f"{products_related_base_url}product-images/{image_id}/"
    try:
        response = requests.delete(url)
        response.raise_for_status()
        messages.success(request, "Image deleted successfully")
    except requests.exceptions.RequestException as e:
        messages.error(request, f"Failed to delete image: {str(e)}")
    return redirect(f'/admin/edit-product/{slug}')

def edit_variant(request, variant_id):
    variant_url = f"{products_related_base_url}variants/{variant_id}/"
    variant_images_url = f"{products_related_base_url}variant-images/"
    
    if request.method == 'GET':
        variant_data = {}
        try:
            response = requests.get(url=variant_url)
            response.raise_for_status()
            variant_data = response.json()
            
            # Fetch product to get its slug for the "Back" button
            if 'product' in variant_data:
                product_url = f"{products_related_base_url}products/{variant_data['product']}/"
                prod_response = requests.get(url=product_url)
                if prod_response.status_code == 200:
                    variant_data['product_slug'] = prod_response.json().get('slug')
                    
        except requests.exceptions.RequestException as e:
            messages.error(request, f"Failed to fetch variant details: {str(e)}")
            return redirect(request.META.get('HTTP_REFERER', '/admin/product-list'))
            
        return render(request, 'edit_variant.html', {"variant": variant_data})
        
    if request.method == 'POST':
        payload = {
            "product": int(request.POST.get('product_id')),
            "name": request.POST.get('name'),
            "price": int(request.POST.get('price')),
            "stock": int(request.POST.get('stock', 0)),
            "compare_at_price": request.POST.get('compare_at_price') or None
        }
        
        try:
            # Update variant details
            response = requests.put(url=variant_url, json=payload)
            response.raise_for_status()
            
            # Handle new images
            new_images = request.FILES.getlist('new_images')
            if new_images:
                for img in new_images:
                    files = {'image': (img.name, img, img.content_type)}
                    payload_img = {'variant': variant_id}
                    img_response = requests.post(url=variant_images_url, files=files, data=payload_img)
                    img_response.raise_for_status()
                    
            messages.success(request, "Variant updated successfully")
        except requests.exceptions.RequestException as e:
            messages.error(request, f"Failed to update variant: {str(e)}")
            
        return redirect(f'/admin/edit-variant/{variant_id}')

def delete_variant_image(request, image_id, variant_id):
    url = f"{products_related_base_url}variant-images/{image_id}/"
    try:
        response = requests.delete(url)
        response.raise_for_status()
        messages.success(request, "Variant image deleted successfully")
    except requests.exceptions.RequestException as e:
        messages.error(request, f"Failed to delete variant image: {str(e)}")
    return redirect(f'/admin/edit-variant/{variant_id}')

def delete_variant(request, variant_id):
    url = f"{products_related_base_url}variants/{variant_id}/"
    if request.method == 'GET':
        try:
            response = requests.delete(url)
            response.raise_for_status()
            messages.success(request, "Variant deleted successfully")
        except requests.exceptions.RequestException as e:
            messages.error(request, f"Failed to delete variant: {str(e)}")
        # Go back to the referring page, which in our case is the edit product page
        return redirect(request.META.get('HTTP_REFERER', '/admin/product-list'))

def delete_product(request,slug):
    delete_product_url=f"{products_related_base_url}products/{slug}/"
    if request.method=='GET':
        try:
            response=requests.delete(url=delete_product_url)
            response.raise_for_status()
            messages.success(request,"product deleted successfully")
        except requests.exceptions.RequestException as e:
            messages.error(request,f"failed to delete the product : {str(e)}")
        return redirect('/admin/product-list')



#batch related  views
def add_batch(request):                     # to add batch
    if request.method=='GET':
        variant_url=products_related_base_url+'variants/'
        batches_url=products_related_base_url+'batches/'
        variants=[]
        batches=[]
        try:
            variant_response=requests.get(url=variant_url)
            variant_response.raise_for_status()
            variants=variant_response.json()
            batches_response=requests.get(url=batches_url)
            batches_response.raise_for_status()
            batches=batches_response.json()
        except requests.exceptions.RequestException as e:
            messages.error(request,f"failed :{str(e)}")
        except ValueError as e:
            messages.error(request, f"Invalid response format: {str(e)}")
        return render(request,'add_batch.html',{"variants":variants,"batches":batches})
    
    if request.method=='POST':
        batches_url=products_related_base_url+'batches/'
        payload={
            
            "variant": int(request.POST.get('variant_id')),
            "qty": int(request.POST.get('qty')),
            "mfg_date": request.POST.get('mfg_date'),
            "exp_date": request.POST.get('exp_date'),
            "is_active": True
        }
        try:
            batches_response=requests.post(url=batches_url,data=payload)
            batches_response.raise_for_status()
            messages.success(request,"Batch added successfully")
        except requests.exceptions.RequestException as e:
            messages.error(request,f"Failed to add batch : {str(e)}")
        return redirect('/admin/add-batch')
    

def delete_batch(request,batch_id):            # to delete batch
    delete_batch_url=f"{products_related_base_url}batches/{batch_id}/"
    if request.method=='GET':
        try:
            response=requests.delete(url=delete_batch_url)
            response.raise_for_status()
            messages.success(request," Batch Deleted Sucessfully")
        except requests.exceptions.RequestException as e:
            messages.error(request,f"unable to delete : str{(e)}")
        return redirect('/admin/add-batch')


def edit_batch(request,batch_id):                   # to edit batch
    edit_batch_url=f"{products_related_base_url}batches/{batch_id}/"
    if request.method=='POST':
        variant_id = request.POST.get('variant_id')
        qty = request.POST.get('qty')
        mfg_date = request.POST.get('mfg_date')
        exp_date = request.POST.get('exp_date')
        payload = {
            "variant": variant_id,
            "qty": qty,
            "mfg_date": mfg_date,
            "exp_date": exp_date
        }
        try:
            response=requests.put(url=edit_batch_url,json=payload)
            print(response.json())
            response.raise_for_status()
            messages.success(request,"Category edited successfully")
        except requests.exceptions.RequestException as e:
            messages.error(request,f"failed to update category : {str(e)}")
        return redirect('/admin/add-batch')

import requests
from django.contrib import messages
from django.shortcuts import render

CART_URL = os.environ.get('CART_URL')

def customer_data(request):
    if request.method=='GET':
        access_token=admin_get_access_token(request)
        if not access_token:
            new_token=admin_refresh_access_token(request)
            if not new_token:
                return admin_if_not_new_token(request)
            access_token=new_token
        # headers={
        #     "Authorization":f"Bearer {access_token}"
        # }

        get_all_customer_url = user_base_url + 'register'
        order_url = f"{CART_URL}admin-get-all-orders/"

        customers = []
        orders = []

        try:
            response = requests.get(get_all_customer_url)
            response.raise_for_status()
            customers = response.json()
        except requests.exceptions.RequestException as e:
            messages.error(request, f"Failed to get customers: {str(e)}")

        try:
            response = requests.get(order_url)
            response.raise_for_status()
            orders = response.json().get("orders", [])
        except requests.exceptions.RequestException as e:
            messages.error(request, f"Failed to fetch orders: {str(e)}")

        
        order_summary = {}

        for order in orders:
            customer_id = order.get("user_id")          # ✅ FIXED
            amount = order.get("total_amount", 0)       # ✅ FIXED

            if not customer_id:
                continue

            if customer_id not in order_summary:
                order_summary[customer_id] = {
                    "total_orders": 0,
                    "total_spend": 0
                }

            order_summary[customer_id]["total_orders"] += 1
            order_summary[customer_id]["total_spend"] += amount


        for customer in customers:
            summary = order_summary.get(customer.get("id"), {})
            customer["total_orders"] = summary.get("total_orders", 0)
            customer["total_spend"] = summary.get("total_spend", 0)

        resp= render(request, "admin_index.html", {
            "customers": customers,
            "orders": orders,
        })
        access_token_expiry = 20 * 60
        resp.set_cookie(
                        "admin_access_token",
                        access_token,
                        max_age=access_token_expiry,
                        httponly=True,
                        secure=False,
                        samesite='lax'
                    )
        return resp

def admin_get_all_orders(request):
    if request.method=='GET':
        access_token=admin_get_access_token(request)
        if not access_token:
            new_token=admin_refresh_access_token(request)
            if not new_token:
                return admin_if_not_new_token(request)
            access_token=new_token
        order_url = f"{CART_URL}admin-get-all-orders/"
        headers = {"Authorization": f"Bearer {access_token}"}
        orders=[]
        try:
            response=requests.get(url=order_url, headers=headers)
            response.raise_for_status()
            orders=response.json()
            messages.success(request,f"oredrs fetched successfully")
        except requests.exceptions.RequestException as e:
            messages.error(request,f"failed to fetch orders data :{str(e)}")
        
        resp= render(request,'orders_list.html',{'orders':orders})
        access_token_expiry = 20 * 60
        resp.set_cookie(
            "admin_access_token",
                        access_token,
                        max_age=access_token_expiry,
                        httponly=True,
                        secure=False,
                        samesite='lax'

        )
        print(f"orders data are\n {orders}")
        return resp

def customer_list_data(request):
    if request.method=='GET':
        access_token=admin_get_access_token(request)
        if not access_token:
            new_token=admin_refresh_access_token(request)
            if not new_token:
                return admin_if_not_new_token(request)
            access_token=new_token
        get_all_customer_url = user_base_url + 'register'
        try:
            response = requests.get(get_all_customer_url)
            response.raise_for_status()
            customers = response.json()
        except requests.exceptions.RequestException as e:
            messages.error(request, f"Failed to get customers: {str(e)}")
        resp= render(request, "customers_list.html", {
            "customers": customers
        })
        return resp


# new endpoints

def deliveries_list(request):
    if request.method == 'GET':
        access_token = admin_get_access_token(request)
        if not access_token:
            new_token = admin_refresh_access_token(request)
            if not new_token: return admin_if_not_new_token(request)
            access_token = new_token
        
        order_url = f"{CART_URL}admin-get-all-orders/"
        headers = {"Authorization": f"Bearer {access_token}"}
        try:
            resp = requests.get(order_url, headers=headers)
            resp.raise_for_status()
            # The 'orders' structure has an inner 'orders' list
            data = resp.json()
            if 'orders' in data and isinstance(data['orders'], list):
                all_orders = data['orders']
            else:
                all_orders = data if isinstance(data, list) else []
                
            deliveries = [o for o in all_orders if o.get('status') in ['PAID', 'SHIPPED', 'DELIVERED']]
        except Exception as e:
            print(e)
            deliveries = []
        return render(request, 'deliveries.html', {'orders': deliveries})

def update_delivery_status(request, order_id):
    if request.method == 'POST':
        access_token = admin_get_access_token(request)
        if not access_token: return admin_if_not_new_token(request)
        new_status = request.POST.get('status')
        url = f"{CART_URL}admin-orders/{order_id}/status/"
        headers = {"Authorization": f"Bearer {access_token}"}
        try:
            requests.patch(url, json={"status": new_status}, headers=headers)
            messages.success(request, "Status updated successfully")
        except:
            messages.error(request, "Failed to update status")
        return redirect('/admin/deliveries')

def toggle_customer(request, pk):
    if request.method == 'POST':
        url = f"{user_base_url}admin/users/{pk}/"
        try:
            requests.patch(url)
            messages.success(request, "Toggled status successfully")
        except:
            messages.error(request, "Failed to toggle status")
        return redirect('/admin/customers-list')

def delete_customer(request, pk):
    if request.method == 'GET':
        url = f"{user_base_url}admin/users/{pk}/"
        try:
            requests.delete(url)
            messages.success(request, "Customer deleted")
        except:
            messages.error(request, "Failed to delete")
        return redirect('/admin/customers-list')

def admin_order_detail(request, order_id):
    if request.method == 'GET':
        access_token = admin_get_access_token(request)
        if not access_token:
            new_token = admin_refresh_access_token(request)
            if not new_token: return admin_if_not_new_token(request)
            access_token = new_token

        order_url = f"{CART_URL}admin-orders/{order_id}/"
        headers = {"Authorization": f"Bearer {access_token}"}
        
        try:
            response = requests.get(url=order_url, headers=headers)
            response.raise_for_status()
            order = response.json()
            return render(request, 'admin_order_detail.html', {'order': order})
        except requests.exceptions.RequestException as e:
            messages.error(request, f"Failed to fetch order details: {str(e)}")
            return redirect('/admin/orders-list')

def transactions_list(request):
    if request.method == 'GET':
        access_token = admin_get_access_token(request)
        if not access_token: return admin_if_not_new_token(request)
        order_url = f"{CART_URL}admin-get-all-orders/"
        try:
            resp = requests.get(order_url)
            resp.raise_for_status()
            orders = resp.json().get('orders', [])
        except:
            orders = []
        return render(request, 'transactions.html', {'orders': orders})

def reviews_list(request):
    if request.method == 'GET':
        access_token = admin_get_access_token(request)
        if not access_token: return admin_if_not_new_token(request)
        url = f"{products_related_base_url}admin-reviews/"
        try:
            resp = requests.get(url)
            resp.raise_for_status()
            reviews = resp.json()
        except:
            reviews = []
        
        # Enrich reviews with product slug for linking
        try:
            all_products = requests.get(f"{products_related_base_url}products/").json()
            pid_to_slug = {p.get('product_id'): p.get('slug', '') for p in all_products}
            for review in reviews:
                review['product_slug'] = pid_to_slug.get(review.get('product'), '')
        except:
            pass
        
        return render(request, 'reviews_admin.html', {'reviews': reviews})

def delete_review(request, review_id):
    if request.method == 'GET':
        access_token = admin_get_access_token(request)
        if not access_token: return admin_if_not_new_token(request)
        url = f"{products_related_base_url}admin-reviews/{review_id}/"
        try:
            requests.delete(url)
            messages.success(request, "Review deleted")
        except:
            messages.error(request, "Failed to delete review")
        return redirect('/admin/reviews-list')
