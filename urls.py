from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

app_name = 'myapp'

urlpatterns = [
    path('', views.car_list, name='car_list'),
    path('car/<int:pk>/', views.car_detail, name='car_detail'),
    path('car/<int:pk>/rent/', views.rent_car, name='rent_car'),
    path('rental/<int:rental_id>/success/', views.rental_success, name='rental_success'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Auth URLs
    path('login/', LoginView.as_view(template_name='myapp/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    
    # Password Reset URLs
    path('password-reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    # Admin Dashboard URLs
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/cars/', views.admin_cars, name='admin_cars'),
    path('admin-dashboard/cars/add/', views.admin_car_add, name='admin_car_add'),
    path('admin-dashboard/cars/<int:pk>/edit/', views.admin_car_edit, name='admin_car_edit'),
    path('admin-dashboard/cars/<int:pk>/delete/', views.admin_car_delete, name='admin_car_delete'),
    path('admin-dashboard/rentals/', views.admin_rentals, name='admin_rentals'),
    path('admin-dashboard/users/', views.admin_users, name='admin_users'),
]