from django.shortcuts import render, HttpResponseRedirect, redirect
from django.http import JsonResponse
from django.db.models import Q
from django.views import View
from .models import Product, Customer, Cart, PlacedOrder
from .forms import RegistrationForm, LoginForm, ChangePasswordForm, CustomerProfile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User

# Home page
class Home(View):
  def get(self, request):
    if not request.user.is_authenticated:
      return HttpResponseRedirect('/login')
    else:
      mtw = Product.objects.filter(category='MTW')
      ftw = Product.objects.filter(category='FTW')
      mbw = Product.objects.filter(category='MBW')
      fbw = Product.objects.filter(category='FBW')
      context = {'mbw': mbw, 'fbw': fbw, 'mtw': mtw, 'ftw': ftw}
      return render(request, 'myapp/home.html', context)
    
# Product page   
class ProductDetails(View):
  def get(self, request, id):
    if not request.user.is_authenticated:
      return HttpResponseRedirect('/login')
    else:
      prod = Product.objects.get(pk=id)
      already_in_cart = False
      if Cart.objects.filter(Q(user=request.user) & Q(product=prod)).exists():
        already_in_cart = True
      return render(request, 'myapp/productdetails.html', {'prod': prod, 'already_in_cart':already_in_cart})

# Mobile Function
def Mobiles(request, data=None):
  if not request.user.is_authenticated:
    return HttpResponseRedirect('/login')
  else:
    if(data == None):
      mobiles = Product.objects.all().filter(category='M')
    elif(data == 'Redmi'):
      mobiles = Product.objects.all().filter(category='M').filter(brand='Redmi')
    elif(data == 'Samsung'):
      mobiles = Product.objects.all().filter(category='M').filter(brand='Samsung')
    elif(data == 'Below'):
      mobiles = Product.objects.all().filter(category='M').filter(discounted_price__lt = 10000)
    elif(data == 'Above'):
      mobiles = Product.objects.all().filter(category='M').filter(discounted_price__gt = 10000)
    return render(request, 'myapp/mobiles.html', {'mobiles': mobiles})
 
# Registration Function
def user_Regi(request):
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      form.save()
      messages.success(request, 'Registration Successful!')
      return HttpResponseRedirect('/login')
  else:
    form = RegistrationForm()
  return render(request, 'myapp/registration.html', {'form':form})
      
# Login Function
def user_Login(request):
  if request.user.is_authenticated:
    return HttpResponseRedirect('/')
  else:
    if request.method == 'POST':
      form = LoginForm(request=request, data=request.POST)
      if form.is_valid():
        uname = form.cleaned_data.get('username')
        upass = form.cleaned_data.get('password')
        validUser = authenticate(username=uname, password=upass)
        if validUser is not None:
          login(request, validUser)
          return HttpResponseRedirect('/')
          messages.success(request, 'Login Successful!')
    else:
      form = LoginForm()
  return render (request, 'myapp/login.html', {'form': form})
  
# User logout
def user_Logout(request):
  logout(request)
  return HttpResponseRedirect('/login')
  
#Change Password Function
def change_Password(request):
  if request.method == 'POST':
    form = ChangePasswordForm(user=request.user, data=request.POST)
    if form.is_valid():
      form.save()
      messages.success(request, 'Password Has Been Changed Successful!')
      return HttpResponseRedirect('/login')
  else:
    form = ChangePasswordForm(request.user)
  return render(request, 'myapp/changepassword.html', {'form':form})
  
# Add To Cart Function
def addToCart(request):
  user = request.user
  present = False
  product_id = request.GET.get('prod_id')
  product = Product.objects.get(id=product_id)
  cart = Cart.objects.filter(user=user)
  for ct in cart:
    if str(ct.product) == str(product):
      present = True
  if not(present):
    Cart(user=user, product=product).save()
  return redirect('/showcart')
  
def showCarts(request):
  user = request.user
  carts = Cart.objects.filter(user=user)
  if carts:
    amount = 0.0
    shippedprice = 70.0
    totalamount = 0.0
    allcart = [c for c in carts if user == request.user]
    for ct in allcart:
      price = ct.quantity * ct.product.discounted_price
      amount += price
      totalamount += price
    finalamount = totalamount+shippedprice
    return render(request, 'myapp/addtocart.html', {'carts':carts, 'finalamount':finalamount, 'amount':amount})
  else:
    return render(request, 'myapp/emptycart.html')

# Add cart plus icons Function
def cart_icon_plus(request):
  if request.method == 'GET':
    prod_id = request.GET.get('prod_id')
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.quantity +=1
    c.save()
    amount = 0.0
    shippedprice = 70.0
    totalamount = 0.0
    user = request.user
    allcart = [c for c in Cart.objects.all().filter(user=user) if user == request.user]
    print(allcart)
    for ct in allcart:
      price = ct.quantity * ct.product.discounted_price
      amount += price
      totalamount += price
    finalamount = totalamount+shippedprice
    data = {
      'quantity': c.quantity,
      'totalamount':totalamount,
      'finalamount': finalamount
    }
    print(data)
    return JsonResponse(data)
    
# Add cart minus icons Function
def cart_icon_minus(request):
  if request.method == 'GET':
    prod_id = request.GET.get('prod_id')
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.quantity -=1
    c.save()
    price = 0.0
    amount = 0.0
    shippedprice = 70.0
    totalamount = 0.0
    user = request.user
    allcart = [p for p in Cart.objects.all() if user == request.user]
    for ct in allcart:
      amount = ct.quantity * ct.product.discounted_price
    totalamount -= amount
    finalamount=totalamount+shippedprice
    data = {
      'quantity': c.quantity,
      'totalamount': totalamount,
      'finalamount': finalamount
    }
    return JsonResponse(data)
  
# Remove Cart items
def RemoveCart(request):
  if request.method == 'GET':
    prod_id = request.GET.get('prod_id')
    print(prod_id)
    c = Cart.objects.get(Q(user=request.user) & Q(product=prod_id))
    c.delete()
  return redirect('/showcart')
  
# Payment Done
def user_payment(request):
  if request.method == 'GET':
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    carts = Cart.objects.filter(user=user)
    for ct in carts:
      PlacedOrder(user=user, customer=customer, product=ct.product, quantity=ct.quantity).save()
      ct.delete()
  return redirect('/order')
  
# Address Function
def user_Address(request):
  adrs = Customer.objects.filter(user=request.user)
  return render(request, 'myapp/address.html', {'adrs':adrs})

# Order Function
def Ordered_Product(request):
  user = request.user
  prod_order = PlacedOrder.objects.filter(user=user)
  return render(request, 'myapp/orders.html', {'prod_order':prod_order})
  
# Profile Function
def user_Profile(request):
  if request.method == 'POST':
    usr = request.user
    print(usr)
    form = CustomerProfile(request.POST)
    if form.is_valid():
      name = form.cleaned_data.get('name')
      locality = form.cleaned_data.get('locality')
      city = form.cleaned_data.get('city')
      state = form.cleaned_data.get('state')
      zipcode = form.cleaned_data.get('zipcode')
      cust = Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode = zipcode)
      cust.save()
      messages.success(request, 'Profile Set Successful!')
      return HttpResponseRedirect('/address')
  else:
    form = CustomerProfile()
  return render(request, 'myapp/profile.html', {'form': form})
  
# Checkout Function
def Checkout(request):
  user = request.user
  address = Customer.objects.filter(user=user)
  cart = Cart.objects.filter(user=user)
  amount = 0.0
  shippedprice = 70.0
  totalamount = 0.0
  user = request.user
  allcart = [p for p in Cart.objects.all() if user == request.user]
  print(allcart)
  for ct in allcart:
    amount = ct.quantity * ct.product.discounted_price
    totalamount += amount
  finalamount=totalamount+shippedprice
  context = {'address':address, 'cart': cart, 'totalamount':totalamount}
  return render(request, 'myapp/checkout.html', context)
  
  
  
  
  