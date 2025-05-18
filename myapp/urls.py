from django.urls import path
from . import views
app_name = 'myapp'
urlpatterns = [
    # Quản lý
    path('menu/quanly/', views.menu_management, name='menu_management'),
    path('menu/quanly/add/', views.add_menu_item, name='add_menu_item'),
    path('menu/quanly/edit/', views.edit_menu_item, name='edit_menu_item'),
    path('menu/quanly/toggle-visibility/', views.toggle_menu_item_visibility, name='toggle_menu_item_visibility'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/create/', views.create_order, name='create_order'),
    path('orders/update_status/', views.update_order_status, name='update_order_status'),

    # Nhân viên
    path('menu/nhanvien/', views.menu_nhanvien, name='menu_nhanvien'),
    path('menu/nhanvien/edit/', views.edit_menu_item_nhanvien, name='edit_menu_item_nhanvien'),
    path('menu/nhanvien/toggle-visibility/', views.toggle_menu_item_visibility_nhanvien,
         name='toggle_menu_item_visibility_nhanvien'),

    # Khách hàng
    path('menu/khachhang/', views.menu_khachhang, name='menu_khachhang'),
    path('menu/khachhang/add-to-cart/', views.add_to_cart, name='add_to_cart'),

    # Chuyển hướng
    path('menu/', views.redirect_based_on_role, name='redirect_based_on_role'),
]