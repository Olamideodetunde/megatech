from django.urls import path

from . import views
urlpatterns = [
    path('',views.index,name='home-page'),
    path('products/<slug:slug>',views.products,name='product-page'),
    path('store',views.store,name='store'),
    path('profile',views.profile,name='profile'),
    path('cart',views.cart,name='cart'),
    path('quantitytoggle/<int:prod_id>',views.quantitytoggle,name='quantitytoggle'),
    path('checkout',views.checkout,name='checkout-page'),
    path('add-cart/<int:product_id>',views.add_cart,name='add-cart'),
    path('remove-cart/<int:product_id>',views.remove_cart,name='remove-cart'),
    path('logout',views.logoutUser,name='logout'),
    path('login',views.LoginView,name='login'),
    path('signup',views.SignupView,name='signup'),
] 
