from django.shortcuts import render,HttpResponseRedirect
from django.http import JsonResponse,HttpResponse
from django.contrib import messages
from django.urls import reverse
from .models import Product,Transaction,Newsletter,Cart,Customer
from .forms import NewsletterForm,SignupForm,LoginForm
# Create your views here.
def index(request):
  form=NewsletterForm()
  all_products=Product.objects.all()
  products_widget=Product.objects.all()[:3]
  second_widget=Product.objects.all()[:3]
  cartcount=Cart.objects.filter(cust_id=request.session.get('loggedin'))
  if request.is_ajax():
    m=Newsletter(email=request.POST['newsletter_email'])
    m.save()
    response='You have Subscribed Successfully'
    return JsonResponse({'success':response})
  return render(request,'ecomtech/index.html',{'form':form,'session': request.session.get('loggedin'),'cartcount':cartcount,'all_products':all_products,'products_widget':products_widget,'second_widget':second_widget})
def checkout(request):
  cartcount=Cart.objects.filter(cust_id=request.session.get('loggedin'))
  return render(request,'ecomtech/checkout.html',{'session':request.session.get('loggedin'),'cartcount':cartcount})
def signup(request):
  form=SignupForm()
  cartcount=Cart.objects.filter(cust_id=request.session.get('loggedin'))
  if request.method=='GET':
    return render(request,'ecomtech/signup.html',{'form':form,'cartcount':cartcount})
  else:
    email=request.POST.get('cust_email')
    password=request.POST.get('cust_password')
    fname=request.POST.get('cust_fname')
    lname=request.POST.get('cust_lname')
    phone=request.POST.get('cust_phone')
    x=Customer(cust_email=email,cust_password=password,cust_fname=fname,cust_lname=lname,cust_phone=phone)
    x.save()
    return HttpResponseRedirect(reverse('login'))
def login(request):
  form=LoginForm()
  cartcount=Cart.objects.filter(cust_id=request.session.get('loggedin'))
  if request.method=='GET':
    return render(request,'ecomtech/login.html',{'form':form,'cartcount':cartcount})
  else:
    email=request.POST.get('cust_email')
    password=request.POST.get('cust_password')
    cust=Customer.objects.filter(cust_email=email, cust_password=password).first()
    if cust:
      request.session['loggedin']= cust.id
      return HttpResponseRedirect(reverse('store'))
    else:
      messages.add_message(request,messages.ERROR,'Wrong Credentials')
      return HttpResponseRedirect(reverse('login'))
def products(request,slug):
  cartcount=Cart.objects.filter(cust_id=request.session.get('loggedin'))
  if request.method== 'GET':
    single_prod=Product.objects.get(slug=slug)
    all_products=Product.objects.all()[:2]
    next_products=Product.objects.all()[2:2]
    return render(request,'ecomtech/product.html',{'session':request.session.get('loggedin'),'cartcount':cartcount,'all_products':all_products,'next_products':next_products,'single_prod':single_prod})
def cart(request):
  if request.method == 'GET':
    cart=Cart.objects.filter(cust_id=request.session.get('loggedin'))
    return render(request,'ecomtech/cart.html',{'session':request.session.get('loggedin'),'cart':cart})
  else :
    pass
def add_cart(request):
  if request.method == 'GET':
    return HttpResponseRedirect(reverse('store'))
  else :
    if request.is_ajax():
      prod_id=request.POST.get('prod_id')
      cust=Customer.objects.get(pk=request.session.get('loggedin'))
      prod=Product.objects.get(pk=prod_id)
      m=Cart(cust_id=cust,product_name=prod)
      m.save()
      response='Item Successfully added'
      return  JsonResponse({'success':response})
    return HttpResponseRedirect(reverse('store'))
def remove_cart(request):
  if request.method == 'GET':
    return HttpResponseRedirect(reverse('store'))
  else :
    return HttpResponseRedirect(reverse('store'))
def store(request):
    cartcount=Cart.objects.filter(cust_id=request.session.get('loggedin'))
    if request.method=='GET':
      all_products=Product.objects.all()
      products_widget=Product.objects.all()[:3]
      cartlist=[]
      for i in cartcount:
        cartlist.append(i)
      return render(request,'ecomtech/store.html',{'all_products':all_products,'products_widget':products_widget,'session':request.session.get('loggedin'),'cartcount':cartcount,'cartlist':cartlist})
def logout(request):
  request.session.pop('loggedin')
  return HttpResponseRedirect(reverse('login'))
