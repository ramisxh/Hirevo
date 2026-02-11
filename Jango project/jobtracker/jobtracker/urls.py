from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from applications.views import dashboard, add_company, signup

urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentication URLs
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='registration/login.html'),
        name='login'
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),

    path('signup/', signup, name='signup'),
    
    # Main application URLs
    path('', dashboard, name='dashboard'),
    path('dashboard/', dashboard, name='dashboard'),
    path('add-company/', add_company, name='add_company'),
]