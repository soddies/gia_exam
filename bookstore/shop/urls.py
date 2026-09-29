from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_views, name='login'),
    path('', views.main_view, name='main'),
    path('logout/', views.logout_view, name='logout'),

    path('product/create/', views.product_create, name='product_create'),
    path('product/<int:product_id>/update/', views.product_update, name='product_update'),
    path('product/<int:product_id>/delete/', views.product_delete, name='product_delete'),

    path('orders/', views.orders_list, name='orders_list'),
]