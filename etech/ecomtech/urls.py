from django.urls import path

from . import views
urlpatterns = [
    path('',views.index,name='home-page'),
    path('products/<slug:slug>',views.products,name='product-page'),
    path('store',views.store,name='store'),
    path('cart',views.cart,name='cart'),
    path('checkout',views.checkout,name='checkout-page'),
    path('remove-cart',views.remove_cart,name='remove-cart'),
    path('login',views.login,name='login'),
    path('signup',views.signup,name='signup'),
] 
