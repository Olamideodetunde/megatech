import logging
from django.shortcuts import render,HttpResponseRedirect,redirect,get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Product,Transaction,Newsletter,Cart,User
from .forms import NewsletterForm,SignupForm,ProfileForm
# Create your views here.
def index(request):
  form=NewsletterForm()
  all_products=Product.objects.all()
  products_widget=Product.objects.all()[:3]
  second_widget=Product.objects.all()[:3]
  if request.user:
    cartcount=Cart.objects.filter(cust_id=request.user.id)
  else:
    cartcount=[]
  if request.method == 'POST':
    m=Newsletter(email=request.POST['newsletter_email'])
    m.save()
    return redirect(reverse('home'))
  return render(request,'ecomtech/index.html',{'form':form,'cartcount':cartcount,'all_products':all_products,'products_widget':products_widget,'second_widget':second_widget})
def checkout(request):
  cartcount=Cart.objects.filter(cust_id=request.user.id)
  return render(request,'ecomtech/checkout.html',{'cartcount':cartcount})

def LoginView(request):
  cartcount=Cart.objects.filter(cust_id=request.user.id)
  if request.user.is_authenticated:
       return redirect(reverse('store'))
  if request.method == 'POST':
    email=request.POST.get('email').lower()
    password=request.POST.get('password')
    user=authenticate(email=email,password=password)
    if user is not None: 
      login(request,user)
      return redirect(reverse('store'))
    else:
      messages.error(request,'Email Address or Password does not exist')
  context={'cartcount':cartcount}
  return render(request,'ecomtech/login.html',context)
  
  
def SignupView(request):
    cartcount=Cart.objects.filter(cust_id=request.user.id)
    if request.user.is_authenticated:
       return redirect(reverse('store'))
    form = SignupForm()
    if request.method == 'POST':
      form=SignupForm(request.POST)
      if form.is_valid():
         user= form.save(commit=False)
         user.password1= form.cleaned_data.get('password1').lower()
         user.save()
         login(request,user)
         return redirect(reverse('store'))
      else:
        # print(form.cleaned_data)
        # logger = logging.getLogger(__name__)
        # logger.error(form.errors)
        messages.error(request,'An error occured during registration')
    return render(request, 'ecomtech/signup.html',{'form':form,'cartcount':cartcount})
def products(request,slug):
  cartcount=Cart.objects.filter(cust_id=request.user.id).all()
  if request.method== 'GET':
    single_prod=Product.objects.get(slug=slug)
    all_products=Product.objects.all()[:2]
    next_products=Product.objects.all()[2:2]
    return render(request,'ecomtech/product.html',{'cartcount':cartcount,'all_products':all_products,'next_products':next_products,'single_prod':single_prod})
def profile(request):
   cartcount=Cart.objects.filter(cust_id=request.user.id).all()
   form=ProfileForm()
   if request.method == 'POST':
      pass
   context={'cartcount':cartcount,'form':form}
   return render(request,'ecomtech/profile.html',context)
@login_required(login_url='login')
def cart(request):
  cart=Cart.objects.filter(cust_id=request.user.id)
  x=[]
  for i in cart:
     x.append(i.total_amt)
  sumtotal=sum(x)
  return render(request,'ecomtech/cart.html',{'session':request.session.get('loggedin'),'cart':cart,'sumtotal':sumtotal})
@login_required(login_url='login')
def add_cart(request,product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(cust_id=request.user,products=product)
    cart.total_amt= float(int(cart.products.product_price) * int(cart.quantity_added))
    cart.save()
    if not created:
        cart.quantity_added += 1
        cart.total_amt= float(int(cart.products.product_price) * int(cart.quantity_added))
        cart.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
@login_required(login_url='login')
def quantitytoggle(request,prod_id):
    quantity = request.POST.get('quantity') 
    product = get_object_or_404(Product, id=prod_id)
    cart = Cart.objects.get(cust_id=request.user,products=product)
    if cart:
        cart.quantity_added =quantity
        cart.total_amt= float(int(cart.products.product_price) * int(cart.quantity_added))
        cart.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
@login_required(login_url='login')
def remove_cart(request,product_id):
    product= get_object_or_404(Product, id=product_id)
    cart= Cart.objects.filter(cust_id=request.user,products=product).first()
    cart.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
def store(request):
    cartcount=Cart.objects.filter(cust_id=request.user.id)
    if request.method=='GET':
      all_products=Product.objects.all()
      products_widget=Product.objects.all()[:3]
      cartlist=[]
      for i in cartcount:
        cartlist.append(i)
      return render(request,'ecomtech/store.html',{'all_products':all_products,'products_widget':products_widget,'cartcount':cartcount,'cartlist':cartlist})
def logoutUser(request):
  logout(request)
  return HttpResponseRedirect(reverse('login'))
