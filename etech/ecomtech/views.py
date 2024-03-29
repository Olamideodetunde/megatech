import logging,requests,random
import datetime,json
from django.db.models import Q
from django.shortcuts import render,HttpResponseRedirect,redirect,get_object_or_404
from django.http import JsonResponse,HttpResponse
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth import authenticate, login,logout,get_user_model
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Product,Transaction,Newsletter,Cart,User,Wishlist,Checkout,Review,ProductManufacturer,ProductCategory
from .forms import NewsletterForm,SignupForm,ProfileForm,ReviewForm
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
    email=request.POST.get('email')
    user=User.objects.filter(email=email)
    if user:
       
       Checkout.objects.create(cust_id=request.user,country=request.POST['country'],zip_code=request.POST['zip-code'],city=request.POST['city'])
       userid = request.user
       refno = int(random.random() * 1000000000)
       request.session['tref'] = refno
       trans = Transaction(trx_customer=userid,trx_refno=refno,trx_totalamt=sumtotal,trx_status='pending',trx_method='cash')
       trans.save()
    else:
       return redirect('login')
    return redirect(reverse('paystack'))
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
    x=[]
    for i in cartcount:
      x.append(i.total_amt)
    total=sum(x)
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
      
    return render(request, 'ecomtech/signup.html',{'form':form,'cartcount':cartcount,'sumtotal':total})
@login_required(login_url='login')
def confirm_purchases(request):
    """The button here takes them to Paystack"""
    cartcount=Cart.objects.filter(cust_id=request.user.id).all()
    transaction_ref = request.session.get('tref')
    records=User.objects.get(id=request.user.id)
    '''Retrieve all the things this user has selected from Purchases table
        save it in a variable and Then send it to the template'''        
    data = Transaction.objects.filter(trx_refno=transaction_ref,trx_customer=request.user.id).first()
    x=[]
    for i in cartcount:
        x.append(i.total_amt)
    sumtotal=sum(x)
    context={'data':data,'records':records,'sumtotal':sumtotal}   
    return render(request,'ecomtech/confirm_payment.html',context)
@login_required(login_url='login')
def paystack(request):
    url='https://api.paystack.co/transaction/initialize'
    userdeets=User.objects.get(id=request.user.id)
    deets=Transaction.objects.filter(trx_refno=request.session.get('tref')).first()
    data={'email':userdeets.email,'amount':deets.trx_totalamt*100,'reference':deets.trx_refno}
    headers={'Content_Type':'application/json','Authorization':'Bearer sk_test_fb58555bf41a08607aca1beff850bae08805faa7'}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    rspjson = json.loads(response.text) 
    return redirect(rspjson['data']['authorization_url'])

@login_required(login_url='login')
def paystack_response(request):
        refno = request.session.get('tref')

        headers = {"Content-Type": "application/json","Authorization":"Bearer sk_test_fb58555bf41a08607aca1beff850bae08805faa7"}

        response = requests.get(f"https://api.paystack.co/transaction/verify/{refno}",headers=headers)
        rspjson = response.json()
        if rspjson['data']['status'] =='success':
            amt = rspjson['data']['amount']
            ipaddress = rspjson['data']['ip_address']
            t = Transaction.objects.filter(trx_refno=refno).first()
            t.trx_status = 'paid'
            t.trx_expiry=datetime.now()+datetime.timedelta(days=30)
            
            return redirect('payment')  
        else:
            t = Transaction.objects.filter(trx_refno=refno).first()
            t.trx_status = 'failed'
            return "Payment Failed" 
def products(request,slug):
  cartcount=Cart.objects.filter(cust_id=request.user.id).all()
  y= Product.objects.filter(slug=slug).first()
  if request.method== 'GET':
    review=ReviewForm()
    single_prod=Product.objects.get(slug=slug)
    review_product=Review.objects.filter(review_for=y.id).all()
    all_products=Product.objects.all()[:2]
    next_products=Product.objects.all()[2:2]
    x=[]
    for i in cartcount:
        x.append(i.total_amt)
    sumtotal=sum(x)
    return render(request,'ecomtech/product.html',{'cartcount':cartcount,'all_products':all_products,'next_products':next_products,'single_prod':single_prod,'sumtotal':sumtotal,'review':review,'review_product':review_product})
  else:
     review_content=request.POST.get('review_content')
     review_email=request.POST.get('review_email')
     review_by=request.POST.get('review_by')
     review_ratings=request.POST.get('rating')
     x=Review(review_by=review_by,review_email=review_email,review_content=review_content,review_ratings=review_ratings,review_for=y)
     x.save()
     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
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
    
    x=[]
    for i in cartcount:
        x.append(i.total_amt)
    sumtotal=sum(x)
    context={'cartcount':cartcount,'form':form,'sumtotal':sumtotal}
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
def review(request):
   review =ReviewForm()
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
# def process_payment(request):
#     # Get the payment details from the user
#     amount = request.POST.get('amount')
#     payer_name = request.POST.get('name')
#     payer_email = request.POST.get('email')
#     payment_description = request.POST.get('description')

#     # Set the Remita API endpoint
#     endpoint = 'https://remitademo.net/payment/v1/query/'

#     # Set the request headers
#     headers = {
#         'Content-Type': 'application/json',
#         'Authorization': 'Bearer <your access token>'
#     }

#     # Set the request data
#     data = {
#         'serviceTypeId': '<your service type ID>',
#         'amount': amount,
#         'payerName': payer_name,
#         'payerEmail': payer_email,
#         'description': payment_description,
#         'orderId': '<your order ID>',
#         'hash': '<your hash>'
#     }

#     # Send the payment request to the Remita API
#     response = requests.post(endpoint, headers=headers, json=data)

#     # If the payment is successful, generate the invoice
#     if response.status_code == 200:
#         # Set the invoice API endpoint
#         invoice_endpoint = 'https://remita.net/remita-explorer-service/api/payment/orders/' + '<your order ID>' + '/complete'

#         # Send the invoice request to the Remita API
#         invoice_response = requests.put(invoice_endpoint, headers=headers)

#         # If the invoice is generated successfully, return a success message
#         if invoice_response.status_code == 200:
#             return HttpResponse('Payment successful. Invoice generated.')

#     # If the payment or invoice generation fails, return an error message
#     return HttpResponse('Payment failed. Please try again.')
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
    q = request.GET.get('q', '')
    z = request.GET.get('z', '')
    
    cartcount = Cart.objects.filter(cust_id=request.user.id)
    
    all_products = Product.objects.all()
    products_widget = Product.objects.all()[:3]
    cartlist = list(cartcount.values('total_amt'))
    sumtotal = sum(item['total_amt'] for item in cartlist)
    
    prod_manufactuer = ProductManufacturer.objects.all()
    prod_category = ProductCategory.objects.all()
    
    if q:
        all_products = all_products.filter(Q(category__prod_category_name=q))
    
    if z:
        all_products = all_products.filter(Q(prod_manufacturer_name__prod_manufacturer_name=z))
    
    return render(request, 'ecomtech/store.html', {
        'all_products': all_products,
        'products_widget': products_widget,
        'cartcount': cartcount,
        'cartlist': cartlist,
        'sumtotal': sumtotal,
        'prod_manufactuer': prod_manufactuer,
        'prod_category': prod_category
    })
def order(request):
    cartcount = Cart.objects.filter(cust_id=request.user.id)
    cartlist = list(cartcount.values('total_amt'))
    sumtotal = sum(item['total_amt'] for item in cartlist)
    orderdeets=Transaction.objects.filter(trx_customer=request.user.id)
    return render(request, 'ecomtech/order.html', {
        'cartcount': cartcount,
        'cartlist': cartlist,
        'sumtotal': sumtotal,
        'orderdeets':orderdeets,
    })
def logoutUser(request):
  logout(request)
  return HttpResponseRedirect(reverse('login'))
