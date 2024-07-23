from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import CustomPasswordResetForm, CustomSetPasswordForm
urlpatterns = [
    path('',views.index,name='home-page'),
    path('products/<slug:slug>',views.products,name='product-page'),
    path('store',views.store,name='store'),
    path('profile',views.profile,name='profile'),
    path('cart',views.cart,name='cart'),
    path('wishlist',views.wishlist,name='wishlist'),
    path('quantitytoggle/<int:prod_id>',views.quantitytoggle,name='quantitytoggle'),
    path('checkout',views.checkout,name='checkout-page'),
    path('order',views.order,name='order-page'),
    path('remove-order/<int:order_id>',views.remove_order,name='remove-order'),
    path('add-cart/<int:product_id>',views.add_cart,name='add-cart'),
    path('remove-cart/<int:product_id>',views.remove_cart,name='remove-cart'),
    path('add-wishlist/<int:product_id>',views.add_wishlist,name='add-wishlist'),
    path('remove-wishlist/<int:product_id>',views.remove_wishlist,name='remove-wishlist'),
    path('logout',views.logoutUser,name='logout'),
    path('login',views.LoginView,name='login'),
    path('signup',views.SignupView,name='signup'),
    path('paystack',views.paystack,name='paystack'),
    path('paystack-response/',views.paystack_response,name='paystack-response'),
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name='ecomtech/registrations/password_reset_form.html',
            form_class=CustomPasswordResetForm,
        ),
        name='password_reset'
    ),
    path(
        'password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='ecomtech/registrations/password_reset_done.html'
        ),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='ecomtech/registrations/password_reset_confirm.html',
            form_class=CustomSetPasswordForm
        ),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='ecomtech/registrations/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
]
