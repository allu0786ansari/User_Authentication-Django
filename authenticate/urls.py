from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from . import views
from .views import activate
urlpatterns = [
    path('', views.index, name="index"),
    path('register/', views.register, name='register'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.logout_view, name='logout'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),


]