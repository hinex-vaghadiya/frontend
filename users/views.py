from django.shortcuts import render,redirect
from django.http import JsonResponse
import requests
from rest_framework.response import Response
from django.contrib import messages
from rest_framework import status
import json
from admin_dashboard.views import products_related_base_url
import os
user_base_url='https://users-1wfh.onrender.com/api/'  #base url for the users backend api
CART_URL=os.environ.get('CART_URL')
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

# Static Pages
def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def blog(request):
    return render(request, 'blog.html')

def faq(request):
    return render(request, 'faq.html')

def get_cart_count(request):
    """Returns the number of items in the user's cart (0 if not authenticated)."""
    access_token = get_access_token(request)
    if not access_token:
        access_token = refresh_access_token(request)
    if not access_token:
        return 0
    try:
        resp = requests.get(url=f"{CART_URL}cart/", headers={"Authorization": f"Bearer {access_token}"})
        resp.raise_for_status()
        cart_data = resp.json()
        if isinstance(cart_data, list):
            return len(cart_data)
        elif isinstance(cart_data, dict):
            items = cart_data.get("items", cart_data.get("cart", []))
            return len(items) if isinstance(items, list) else 0
    except Exception:
        pass
    return 0


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
    cart_count = get_cart_count(request) if is_authenticated else 0
    context = {
        "is_authenticated": is_authenticated,
        "products": products,
        "cart_count": cart_count,
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
            
            resp= render(request,'profile.html',{"profile":profile_data, "active_tab": "dashboard"})
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
        categories=[]
        url=products_base_url+'products'
        try:
            response=requests.get(url=url)
            response.raise_for_status()
            products=response.json()
        except requests.exceptions.RequestException as e:
            messages.error(request,f"failed to fetch {str(e)}")
        # Fetch categories
        try:
            cat_resp=requests.get(url=products_base_url+'categories/')
            cat_resp.raise_for_status()
            categories=cat_resp.json()
        except:
            pass
        cart_count = get_cart_count(request) if is_authenticated else 0
        return render(request,'shop.html',{"products":products,"categories":categories,"is_authenticated": is_authenticated,"cart_count": cart_count})


def product_detail(request,slug):       # product deatil page using slug 
    resp=check_is_authentictated(request)
    if resp.status_code==200:
        data=json.loads(resp.content.decode("utf-8"))
        is_authenticated=(data["is_authenticated"])
    else:
        is_authenticated=False
    product_detail_url=products_base_url+f"products/{slug}"
    reviews_url = products_base_url + f"{slug}/reviews/"
    product=[]
    reviews=[]
    try:
        response=requests.post(url=product_detail_url)
        response.raise_for_status()
        product=response.json()
    except requests.exceptions.RequestException as e:
        messages.error(request,f"failed to fetch product detail : {str(e)}")
    
    try:
        rev_resp = requests.get(url=reviews_url)
        rev_resp.raise_for_status()
        reviews = rev_resp.json()
    except:
        pass
    
    # Paginate reviews (7 per page)
    page = int(request.GET.get('page', 1))
    per_page = 7
    total_reviews = len(reviews)
    total_pages = max(1, (total_reviews + per_page - 1) // per_page)
    page = max(1, min(page, total_pages))
    start = (page - 1) * per_page
    paginated_reviews = reviews[start:start + per_page]
    
    # Check if user has purchased this product
    has_purchased = False
    if is_authenticated:
        try:
            access_token = get_access_token(request)
            if not access_token:
                access_token = refresh_access_token(request)
            if access_token:
                order_resp = requests.get(
                    url=f"{CART_URL}get-all-orders/",
                    headers={"Authorization": f"Bearer {access_token}"}
                )
                order_resp.raise_for_status()
                orders_data = order_resp.json()
                for order in orders_data.get("orders", []):
                    for item in order.get("items", []):
                        if item.get("product_slug") == slug or item.get("product_name", "").lower() == slug.replace("-", " "):
                            has_purchased = True
                            break
                    if has_purchased:
                        break
        except:
            pass
        
    cart_count = get_cart_count(request) if is_authenticated else 0
    return render(request,'product-detail.html',{
        "product":product,
        "reviews":paginated_reviews,
        "total_reviews": total_reviews,
        "current_page": page,
        "total_pages": total_pages,
        "page_range": range(1, total_pages + 1),
        "is_authenticated": is_authenticated,
        "has_purchased": has_purchased,
        "cart_count": cart_count
    })


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

    cart_count = get_cart_count(request) if is_authenticated else 0
    return render(request,"shop.html",{"products": products,"category_name": slug,"is_authenticated": is_authenticated,"cart_count": cart_count})

cart_url="cart/"

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
        url=f"{CART_URL}cart/add/"
        try:
            print('in try')
            quantity = int(request.POST.get("quantity", 1))
            response=requests.post(url=url,headers=headers,json={"variant_id": request.POST.get("variant_id"),"product_slug": request.POST.get("product_slug"),"quantity": quantity,})
            response.raise_for_status()
            print(f"response{response.json()}")
        except requests.exceptions.RequestException as e:
            messages.error(request,f"failed to add to cart : {str(e)}")
        return redirect(request.META.get('HTTP_REFERER', '/'))
    

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
            cart_resp=requests.get(url=f"{CART_URL}cart/",headers={"Authorization": f"Bearer {access_token}"})
            if cart_resp.status_code == 401:
                access_token = refresh_access_token(request)
                if not access_token:
                    return if_not_new_token(request)
                cart_resp=requests.get(url=f"{CART_URL}cart/",headers={"Authorization": f"Bearer {access_token}"})
            cart_resp.raise_for_status()
            cart_data = cart_resp.json()
        except requests.exceptions.RequestException as e:
            messages.error(request,f"failed to fetch cart : {str(e)}")
        
        # Enrich cart items with product images from Products API
        if cart_data and isinstance(cart_data, dict) and cart_data.get('items'):
            try:
                all_products = requests.get(url=products_base_url + 'products/').json()
                # Build product_name -> primary image URL map
                product_image_map = {}
                for product in all_products:
                    p_name = product.get('product_name', '').strip().lower()
                    p_slug = product.get('slug', '')
                    images = product.get('images', [])
                    # Try to get primary image first, then fall back to first image
                    img_url = ''
                    for img in images:
                        if img.get('is_primary'):
                            img_url = img.get('image', '')
                            break
                    if not img_url and images:
                        img_url = images[0].get('image', '')
                    if img_url:
                        product_image_map[p_name] = img_url
                        product_image_map[p_slug] = img_url
                # Attach image to each cart item
                for item in cart_data['items']:
                    p_name = item.get('product_name', '').strip().lower()
                    p_slug = item.get('product_slug', '')
                    image = product_image_map.get(p_slug) or product_image_map.get(p_name) or ''
                    item['image_url'] = image
            except:
                pass
        
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
        cart_item_delete_url=f"{CART_URL}cart/item/{item_id}/delete/"
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
            cart_update_url=f"{CART_URL}cart/item/{item_id}/update/"
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
        checkout_url=f"{CART_URL}checkout/"
        context={}
        try:
            response=requests.post(url=checkout_url,headers=headers)
            response.raise_for_status()
            checkout_data=response.json()
            context = {
            "checkout_data": [checkout_data]  # wrap in list
            }
            print(f" the checkout data\n {checkout_data}")
        except requests.exceptions.RequestException as e:
            messages.error(request,f"failed during checkout : {str(e)}")
        return render(request,'payment.html',context)




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

        order_url=f"{CART_URL}get-all-orders/"
        context={}
        try:
            response=requests.get(url=order_url,headers=headers)
            response.raise_for_status()
            orders=response.json()
            context = {
            "orders": orders["orders"],
            "active_tab": "orders"  
            }
            print(f"the orders is \n {orders}")
        except requests.exceptions.RequestException as e:
            messages.error(request,f"failed to fetch orders : {str(e)}")
        return render(request,'profile.html',context)

payment_url=f'{CART_URL}order/'
def process_upi_payment(request):
    if request.method=='POST':
        access_token=get_access_token(request)
        if not access_token:
            new_token=refresh_access_token(request)
            if not new_token:
                return if_not_new_token(request)
            access_token=new_token
        

        headers={
            "Authorization":f"Bearer {access_token}"
        }
        context={}
        try:
            id=request.POST.get('id')
            total_amount=request.POST.get('total_amount')
            print(f"id :{id}")
            url=payment_url+id+'/pay/'
            
            domain = request.build_absolute_uri('/')[:-1]
            payload = {
                'success_url': f"{domain}/payment-success?session_id={{CHECKOUT_SESSION_ID}}",
                'cancel_url': f"{domain}/payment-cancel"
            }
            
            response=requests.post(url=url,headers=headers, json=payload)
            response.raise_for_status()
            print(f"response\n {response}")
            
            response_data = response.json()
            checkout_url = response_data.get("checkout_url")
            if checkout_url:
                resp = redirect(checkout_url)
                resp.set_cookie('current_order_id', id, max_age=3600, httponly=True, samesite='lax')
                return resp
            else:
                return JsonResponse({"error": "No checkout_url provided", "raw_response": response_data})
        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": f"Failed during payment: {str(e)}", "response_text": getattr(e.response, 'text', '') if hasattr(e, 'response') else ''})
        return redirect('/cart')


def cancel_order(request):
    if request.method=='POST':
        access_token=get_access_token(request)
        if not access_token:
            new_token=refresh_access_token(request)
            if not new_token:
                return if_not_new_token(request)
            access_token=new_token
        

        headers={
            "Authorization":f"Bearer {access_token}"
        }
        context={}
        try:
            id=request.POST.get('id')
            total_amount=request.POST.get('total_amount')
            print(f"id :{id}")
            url=payment_url+id+'/cancel/'
            response=requests.post(url=url,headers=headers)
            response.raise_for_status()
            print(f"response\n {response}")
        except requests.exceptions.RequestException as e:
            messages.error(request,f"failed during payment : {str(e)}")
        return render(request, 'success_cancel.html', {'status': 'cancel', 'total_amount': total_amount})

def payment_success(request):
    order_id = request.COOKIES.get('current_order_id')
    if not order_id:
        messages.error(request, "No active order found.")
        return redirect('/cart')
    return render(request, 'payment_success_poll.html', {'order_id': order_id})

def check_payment_status(request, order_id):
    access_token = get_access_token(request)
    if not access_token:
        new_token = refresh_access_token(request)
        if not new_token:
            return JsonResponse({'status': 'UNAUTHENTICATED'}, status=401)
        access_token = new_token
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    url = f"{CART_URL}order/{order_id}/pay/status/"
    try:
        response = requests.get(url=url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return JsonResponse(data)
    except requests.exceptions.RequestException as e:
        return JsonResponse({'status': 'ERROR', 'message': str(e)}, status=500)

def payment_cancel(request):
    return render(request, 'success_cancel.html', {'status': 'cancel', 'total_amount': 0})

def submit_review(request, slug):
    if request.method == 'POST':
        user_id = request.COOKIES.get('user_id')
        if not user_id:
            messages.error(request, "Please log in to submit a review.")
            return redirect(f'/product-detail/{slug}')
            
        rating = request.POST.get('rating')
        review_text = request.POST.get('review_text')
        
        url = f"{products_related_base_url}{slug}/reviews/add/"
        payload = {"rating": int(rating), "review_text": review_text, "user_id": int(user_id)}
        print(f"[REVIEW] POST {url} payload={payload}")
        
        try:
            response = requests.post(url, json=payload)
            print(f"[REVIEW] Response status={response.status_code} body={response.text[:500]}")
            response.raise_for_status()
            messages.success(request, "Review submitted successfully!")
        except requests.exceptions.RequestException as e:
            err = "Failed to submit review."
            try:
                resp_data = response.json()
                err = resp_data.get('error', resp_data.get('detail', str(resp_data)))
            except: pass
            print(f"[REVIEW] ERROR: {err}")
            messages.error(request, err)
            
        return redirect(f'/product-detail/{slug}')


def user_invoice(request, order_id):
    if request.method == 'GET':
        access_token = get_access_token(request)
        if not access_token:
            new_token = refresh_access_token(request)
            if not new_token: return if_not_new_token(request)
            access_token = new_token
            
        order_url = f"{CART_URL}order/{order_id}/"
        headers = {"Authorization": f"Bearer {access_token}"}
        
        try:
            response = requests.get(url=order_url, headers=headers)
            response.raise_for_status()
            order = response.json()
            return render(request, 'invoice.html', {'order': order})
        except requests.exceptions.RequestException as e:
            messages.error(request, f"Failed to fetch order details: {str(e)}")
            return redirect('/profile')
