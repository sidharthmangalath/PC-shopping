from django.urls import path
from .import views


urlpatterns = [
    path('', views.index, name='index'),
    path('details/<int:id>', views.computer_detail, name="details"), 
    path('wishlist_toggle/<int:computerId>', views.wishlist_toggle, name="wishlist_toggle"),

    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout')
]