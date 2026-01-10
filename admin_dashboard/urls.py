from django.urls import path,include
from admin_dashboard.views import admin_index,admin_login,admin_verify_login,admin_logout,add_category,edit_category,delete_category,add_product,add_batch,product_list,delete_product,delete_batch,edit_batch,edit_product
urlpatterns = [
    path('', admin_index,name='admin_index'),
    path('login/', admin_login,name='admin_login'),
    path('logout/', admin_logout,name='admin_logout'),
    path('admin_verify_login/', admin_verify_login,name='admin_verify_login'),
    path('add-category/',add_category,name='add_category'),
    path('edit-category/<int:category_id>/',edit_category,name='edit_category'),
    path('delete-category/<int:category_id>/',delete_category,name='delete_category'),
    path('add-product/',add_product,name='add_product'),
    path('add-batch/',add_batch,name='add_batch'),
    path('product-list',product_list,name='product_list'),
    path('delete-product/<int:product_id>/',delete_product,name='delete_product'),
    path('delete-batch/<int:batch_id>/',delete_batch,name='delete_batch'),
    path('edit-batch/<int:batch_id>/',edit_batch,name='edit_batch'),
    path('edit-product/<int:product_id>/',edit_product,name='edit_product'),
    
    
]
