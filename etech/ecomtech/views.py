import logging,requests
from django.shortcuts import render,HttpResponseRedirect,redirect,get_object_or_404
from django.http import JsonResponse,HttpResponse
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth import authenticate, login,logout,get_user_model
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Product,Transaction,Newsletter,Cart,User,Wishlist
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
  x=[]
  for i in cartcount:
     x.append(i.total_amt)
  sumtotal=sum(x)
  return render(request,'ecomtech/index.html',{'form':form,'cartcount':cartcount,'all_products':all_products,'products_widget':products_widget,'second_widget':second_widget,'sumtotal':sumtotal})
@login_required(login_url='login')
def checkout(request):
  cust = get_user_model()
  user= cust.objects.get(id=request.user.id)
  cartcount=Cart.objects.filter(cust_id=request.user.id)
  x=[]
  for i in cartcount:
     x.append(i.total_amt)
  sumtotal=sum(x)
  if request.method=='POST':
     return redirect(reverse('confirm_purchases'))
  return render(request,'ecomtech/checkout.html',{'cartcount':cartcount,'sumtotal':sumtotal,'cust':user})

def LoginView(request):
  cartcount=Cart.objects.filter(cust_id=request.user.id)
  if request.user.is_authenticated:
       return redirect(reverse('store'))
  if request.method == 'POST':
    email=request.POST.get('email').lower()
    password=request.POST.get('password')
    user=authenticate(email=email,password=password)
    if user.is_staff == False:
      if user is not None: 
        login(request,user)
        return redirect(reverse('store'))
      else:
        messages.error(request,'Email Address or Password does not exist')
    else:
       messages.error(request,'Email Address or Password does not exist')
       return redirect(reverse('login'))
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
  if request.method == 'POST':
    form = ProfileForm(request.POST,request.FILES, instance=request.user)
    context={'cartcount':cartcount,'form':form}
    if form.is_valid():
      form.save()
      return redirect('profile')
    else:
      messages.error(request,'An error occured during update')
      return redirect('profile')
  else:
    form = ProfileForm(instance=request.user)
    context={'cartcount':cartcount,'form':form}
    return render(request, 'ecomtech/profile.html', context)
  
  # form=ProfileForm()
  #  if request.method == 'POST':
  #     form=ProfileForm(request.POST, request.FILES)
  #     if form.is_valid():
  #       form.save()
  #  context={'cartcount':cartcount,'form':form}
  #  return render(request,'ecomtech/profile.html',context)
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
def process_payment(request):
    # Get the payment details from the user
    amount = request.POST.get('amount')
    payer_name = request.POST.get('name')
    payer_email = request.POST.get('email')
    payment_description = request.POST.get('description')

    # Set the Remita API endpoint
    endpoint = 'https://remita.net/remita-explorer-service/payment'

    # Set the request headers
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer <your access token>'
    }

    # Set the request data
    data = {
        'serviceTypeId': '<your service type ID>',
        'amount': amount,
        'payerName': payer_name,
        'payerEmail': payer_email,
        'description': payment_description,
        'orderId': '<your order ID>',
        'hash': '<your hash>'
    }

    # Send the payment request to the Remita API
    response = requests.post(endpoint, headers=headers, json=data)

    # If the payment is successful, generate the invoice
    if response.status_code == 200:
        # Set the invoice API endpoint
        invoice_endpoint = 'https://remita.net/remita-explorer-service/api/payment/orders/' + '<your order ID>' + '/complete'

        # Send the invoice request to the Remita API
        invoice_response = requests.put(invoice_endpoint, headers=headers)

        # If the invoice is generated successfully, return a success message
        if invoice_response.status_code == 200:
            return HttpResponse('Payment successful. Invoice generated.')

    # If the payment or invoice generation fails, return an error message
    return HttpResponse('Payment failed. Please try again.')
@login_required(login_url='login')
def add_wishlist(request,product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist= Cart.objects.create(cust_id=request.user,products=product)
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
@login_required(login_url='login')
def remove_wishlist(request,product_id):
    product= get_object_or_404(Product, id=product_id)
    wishlist= Wishlist.objects.filter(cust_id=request.user,products=product).first()
    wishlist.delete()
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
