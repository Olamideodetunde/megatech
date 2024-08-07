import logging,requests,random,traceback
import datetime,json
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q,Count
from django.shortcuts import render,HttpResponseRedirect,redirect,get_object_or_404
from django.http import JsonResponse,HttpResponse
from django.contrib.auth import authenticate, login,logout,get_user_model
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from forex_python.converter import CurrencyRates
from django.contrib.auth.decorators import login_required
from .models import Product,Transaction,Newsletter,Cart,User,Wishlist,Checkout,Review,ProductManufacturer,ProductCategory
from .forms import LoginForm, NewsletterForm,SignupForm,ProfileForm,ReviewForm,CheckoutForm

logger = logging.getLogger(__name__)
# Create your views here.
def index(request):
  form=NewsletterForm()
  all_products=Product.objects.all()
  products_widget=Product.objects.all()[:3]
  second_widget=Product.objects.all()[:3]
  if request.user:
    cartcount=Cart.objects.filter(cust_id=request.user.id)
    wishlist=Wishlist.objects.filter(wishers_deets=request.user.id)
  else:
    cartcount=[]
    wishlist=[]
  if request.method == 'POST':
    m=Newsletter(email=request.POST['newsletter_email'])
    m.save()
    return redirect(reverse('home'))
  x=[]
  for i in cartcount:
     x.append(i.total_amt)
  sumtotal=sum(x)
  return render(request,'ecomtech/index.html',{'form':form,'cartcount':cartcount,'wishlist':wishlist,'all_products':all_products,'products_widget':products_widget,'second_widget':second_widget,'sumtotal':sumtotal})
@login_required(login_url='login')
def checkout(request):
    cust = get_user_model()
    user = cust.objects.get(id=request.user.id)
    cartcount = Cart.objects.filter(cust_id=request.user.id)
    form = CheckoutForm()
    wishlist = Wishlist.objects.filter(wishers_deets=request.user.id)
    x = []
    for i in cartcount:
        x.append(i.total_amt)
    sumtotal = sum(x)
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.get(id=request.user.id)
        if user:
            Checkout.objects.create(cust_id=request.user, country=request.POST['checkout_country'], zip_code=request.POST['checkout_zip'], city=request.POST['checkout_city'])
            userid = request.user
            refno = int(random.random() * 1000000000)
            request.session['tref'] = refno
            trans = Transaction(trx_customer=userid, trx_refno=refno, trx_totalamt=sumtotal, trx_status='pending', trx_method='cash')
            trans.save()
        else:
            return redirect('login')
        return redirect(reverse('paystack'))
    return render(request, 'ecomtech/checkout.html', {'cartcount': cartcount, 'sumtotal': sumtotal, 'cust': user, 'wishlist': wishlist, 'form': form})


def LoginView(request):
    form = LoginForm(request.POST or None)
    cartcount = Cart.objects.filter(cust_id=request.user.id) if request.user.is_authenticated else []
    wishlist = Wishlist.objects.filter(wishers_deets=request.user.id) if request.user.is_authenticated else []

    if request.user.is_authenticated:
        return redirect(reverse('store'))

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)

        if user is not None:
            if not user.is_staff:
                login(request, user)
                return redirect(reverse('store'))
            else:
                messages.error(request, 'Staff users are not allowed to login here.')
        else:
            messages.error(request, 'Email Address or Password does not exist')

    context = {'cartcount': cartcount, 'form': form, 'wishlist': wishlist}
    return render(request, 'ecomtech/login.html', context)



def SignupView(request):
    cartcount=Cart.objects.filter(cust_id=request.user.id)
    wishlist=Wishlist.objects.filter(wishers_deets=request.user.id)
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

    return render(request, 'ecomtech/signup.html',{'form':form,'cartcount':cartcount,'sumtotal':total ,'wishlist':wishlist})
@login_required(login_url='login')
def paystack(request):
    url = 'https://api.paystack.co/transaction/initialize'
    userdeets = User.objects.get(id=request.user.id)
    deets = Transaction.objects.filter(trx_refno=request.session.get('tref')).first()

    if not deets:
        logger.error('Transaction details not found for reference number: %s', request.session.get('tref'))
        return JsonResponse({'error': 'Transaction details not found.'}, status=404)

    trx_totalamt = float(deets.trx_totalamt)

    # Convert USD to NGN using forex-python
    currency_converter = CurrencyRates()
    try:
        trx_totalamt_naira = currency_converter.convert('USD', 'NGN', trx_totalamt)
    except Exception as e:
        static_rate= 1500
        trx_totalamt_naira=trx_totalamt*static_rate
        logger.error('Currency conversion error: %s', str(e))

    amount = int(trx_totalamt_naira * 100)

    data = {
        'email': userdeets.email,
        'amount': amount,
        'reference': deets.trx_refno
    }
    headers = {
        'Content-Type': 'application/json',
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    try:
        rspjson = response.json()
        if 'data' in rspjson and 'authorization_url' in rspjson['data']:
            request.session['tref'] = deets.trx_refno
            return redirect(rspjson['data']['authorization_url'])
        else:
            return JsonResponse({'error': 'Invalid response from Paystack'}, status=400)
    except KeyError as e:
        logger.error(f"KeyError: {e}")
        return JsonResponse({'error': 'Unexpected response format from Paystack'}, status=500)
    except Exception as e:
        logger.error(f"Exception: {e}")
        return JsonResponse({'error': 'An error occurred'}, status=500)
@login_required(login_url='login')
def paystack_response(request):
    refno = request.session.get('tref')

    if not refno:
        return HttpResponse("Transaction reference not found in session", status=400)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"
    }

    try:
        response = requests.get(f"https://api.paystack.co/transaction/verify/{refno}", headers=headers)
        response.raise_for_status()
        rspjson = response.json()

        if rspjson.get('data', {}).get('status') == 'success':
            amt = rspjson['data']['amount']
            ipaddress = rspjson['data']['ip_address']

            t = Transaction.objects.filter(trx_refno=refno).first()
            if not t:
                return HttpResponse("Transaction not found", status=404)

            t.trx_status = 'paid'
            t.trx_expiry = timezone.now() + timedelta(days=30)
            t.save()

            return redirect(reverse('order-page'))
        else:
            t = Transaction.objects.filter(trx_refno=refno).first()
            if t:
                t.trx_status = 'failed'
                t.save()
            return HttpResponse("Payment Failed", status=400)

    except requests.RequestException as e:
        # Handle request exception
        print(f"RequestException: {e}")
        return HttpResponse("Error verifying transaction", status=500)
    except KeyError as e:
        # Handle missing data in response
        print(f"KeyError: {e} - Response: {rspjson}")
        return HttpResponse("Unexpected response format from Paystack", status=500)
    except Exception as e:
        # Handle any other exceptions
        print(f"Exception: {e}")
        print(traceback.format_exc())  # Print the stack trace
        return HttpResponse("An error occurred", status=500)
def products(request,slug):
  cartcount=Cart.objects.filter(cust_id=request.user.id).all()
  wishlist=Wishlist.objects.filter(wishers_deets=request.user.id)
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
    return render(request,'ecomtech/product.html',{'cartcount':cartcount,'all_products':all_products,'next_products':next_products,'single_prod':single_prod,'sumtotal':sumtotal,'review':review,'review_product':review_product,'wishlist':wishlist})
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
  wishlist=Wishlist.objects.filter(wishers_deets=request.user.id)
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
    context={'cartcount':cartcount,'form':form,'sumtotal':sumtotal,'wishlist':wishlist}
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
  wishlist=Wishlist.objects.filter(wishers_deets=request.user.id)
  x=[]
  for i in cart:
     x.append(i.total_amt)
  sumtotal=sum(x)
  return render(request,'ecomtech/cart.html',{'session':request.session.get('loggedin'),'cart':cart,'sumtotal':sumtotal,'wishlist':wishlist})
@login_required(login_url='login')
def wishlist(request):
  cart=Cart.objects.filter(cust_id=request.user.id)
  wishlist=Wishlist.objects.filter(wishers_deets=request.user.id)
  x=[]
  for i in cart:
     x.append(i.total_amt)
  sumtotal=sum(x)
  return render(request,'ecomtech/wishlist.html',{'session':request.session.get('loggedin'),'cart':cart,'sumtotal':sumtotal,'wishlist':wishlist})
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
def add_wishlist(request,product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist= Wishlist.objects.create(wishers_deets=request.user,product_name=product)
    product.added_to_wishlist=True
    product.save()
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
    wishlist= Wishlist.objects.filter(wishers_deets=request.user,product_name=product).first()
    wishlist.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='login')
def remove_order(request,order_id):
    order= Transaction.objects.filter(id=order_id).first()
    order.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
def store(request):
    q = request.GET.get('q', '')
    z = request.GET.get('z', '')
    min_price = request.GET.get('min_price', 0)
    max_price = request.GET.get('max_price', 15000)
    print(f"Min Price: {min_price}, Max Price: {max_price}")
    cartcount = Cart.objects.filter(cust_id=request.user.id)
    wishlist = Wishlist.objects.filter(wishers_deets=request.user.id)
    all_products = Product.objects.all()
    products_widget = Product.objects.all()[:3]
    cartlist = list(cartcount.values('total_amt'))
    sumtotal = sum(item['total_amt'] for item in cartlist)

    prod_manufactuer = ProductManufacturer.objects.annotate(product_count=Count('prod_manufact'))
    prod_category = ProductCategory.objects.annotate(product_count=Count('prod_category'))

    if q:
        all_products = all_products.filter(Q(category__prod_category_name=q))

    if z:
        all_products = all_products.filter(Q(prod_manufacturer_name__prod_manufacturer_name=z))

    if min_price:
        all_products = all_products.filter(product_price__gte=min_price)

    if max_price:
        all_products = all_products.filter(product_price__lte=max_price)

    return render(request, 'ecomtech/store.html', {
        'all_products': all_products,
        'products_widget': products_widget,
        'cartcount': cartcount,
        'cartlist': cartlist,
        'sumtotal': sumtotal,
        'prod_manufactuer': prod_manufactuer,
        'prod_category': prod_category,
        'wishlist': wishlist,
    })
def order(request):
    cartcount = Cart.objects.filter(cust_id=request.user.id)
    cartlist = list(cartcount.values('total_amt'))
    wishlist=Wishlist.objects.filter(wishers_deets=request.user.id)
    sumtotal = sum(item['total_amt'] for item in cartlist)
    orderdeets=Transaction.objects.filter(trx_customer=request.user.id)
    return render(request, 'ecomtech/order.html', {
        'cartcount': cartcount,
        'cartlist': cartlist,
        'sumtotal': sumtotal,
        'orderdeets':orderdeets,
        'wishlist':wishlist
    })
def logoutUser(request):
  logout(request)
  return HttpResponseRedirect(reverse('login'))
