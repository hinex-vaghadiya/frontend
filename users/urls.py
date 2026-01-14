from django.urls import path,include
from users.views import home,login,index,verify_login,profile,logout,register,verify_register,profile_update,shop,product_detail
urlpatterns = [
    path('', index,name='index'),
    path('login/',login,name='login'),
    path('verify_login/',verify_login,name='verify_login'),
    path('home/',home,name='home'),
    path('profile/',profile,name='profile'),
    path('logout/',logout,name='logout'),
    path('register/',register,name='register'),
    path('verify_register/',verify_register,name='verify_register'),
    path('profile-update/',profile_update,name="profile-update"),
    path('shop/',shop,name='shop'),
    path('/product-detail/<int:product_id>',product_detail,name='product-detail')
    
]
