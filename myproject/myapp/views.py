from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as auth_login,logout,update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .models import product,Cart,Order
from django.db.models import Q
import razorpay




# Create your views here.
def index (request):
    context={}
    products=product.objects.filter(category=int("1"))
    productss=product.objects.filter(category=int("2"))
    productsss=product.objects.filter(category=int("3"))
    context["products"]=products
    context["productss"]=productss
    context["productsss"]=productsss

    return render(request,'index.html',context)

def contact(request):
    return render(request,'contact.html')


def register (request):
    context={}
    if request.method=='POST':
        u=request.POST['uname']
        m=request.POST['mnumber']
        e=request.POST['eemail']
        a=request.POST['aage']
        p=request.POST['pass']
        c=request.POST['cpass']
        if u=="" or m=="" or e=="" or a=="" or p=="" or c=="":
            context['error_message']="Filed cant be empty please fill all filed"
            return render (request,'register.html',context)
        elif p!=c:
            context["error_message"]="Filed password not match"
            return render(request,'register.html',context)
        else:
            u=User.objects.create(username=u,email=e,first_name=m)
            u.set_password(p)
            u.save()
            context["success"]="Registration Successful!!!!! U can Login NOw"
            return render (request,'register.html',context)

    else:
        return render (request,'register.html')
    return render (request,'register.html')



def login(request):
    context={}
    if request.method=="POST":
        u=request.POST['uname']
        p=request.POST['pass']
        if p=="" or u=="":
            context["error_message"]="Filed cant be empty please fill vaild first name and password" 
            return render(request,'login.html',context)
        else:
            u=authenticate(username=u,password=p)
            if u is not None:
                auth_login(request,u)
                return redirect('/index')
            else:
                context['error_message']="username and pass not match"
                return render(request,'login.html',context)


    
    return render (request,'login.html')

def change_pass(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            fm=PasswordChangeForm(user=request.user,data=request.POST)
            if fm.is_valid():
                fm.save()
                update_session_auth_hash(request,fm.user)
                context={}
                context["err"]="Your password has been change" 
                return redirect('/index',context)
        else:
            fm=PasswordChangeForm(user=request.user)
        return render (request, 'change_pass.html',{'fm':fm}) 
    else:
        return redirect("/login")


def ulogout(request):
    logout(request)
    return redirect('/index')



def shopbycategory(request,cid):
    products=product.objects.filter(sub_category=int(cid))
    context = {
        'products': products,
    }
    return render (request,"category.html",context)

def filterbycategory(request,cid):
    products=product.objects.filter(category=int(cid))
    context={}
    context["products"]=products
    return render (request,"filterby.html",context)

def filterbyprice(request):
    l=request.GET["min"]
    h=request.GET["max"]
    q1=Q(price__gte=l)
    q2=Q(price__lte=h)
    products=product.objects.filter(q1&q2,category=int("1"))
    productss=product.objects.filter(q1&q2,category=int("2"))
    productsss=product.objects.filter(q1&q2,category=int("3"))
    
    
    
    context={'products':products,
    'productss':productss,
    'productss':productsss
    }
    return render (request,'index.html',context)




def sortbyprice(request,s):
    context={}
    if s=="0":
        context["err"]="Your password has been change" 
        products=product.objects.order_by("-price").filter(category=int("1"))
        productss=product.objects.order_by("-price").filter(category=int("2"))
        productsss=product.objects.order_by("-price").filter(category=int("3"))

    else:
        context["erre"]="Your password has been changed" 
        products=product.objects.order_by("price").filter(category=int("1"))
        productss=product.objects.order_by("price").filter(category=int("2"))
        productsss=product.objects.order_by("price").filter(category=int("3"))
    context["products"]=products
    context["productss"]=productss
    context["productsss"]=productsss    
  
    return render (request,"index.html",context)


def product_details(request,pid):
    products=product.objects.filter(id=pid)
    productss=product.objects.all()

    context = {
        'products': products,
        'productss': productss
    }
    return render(request,"product_details.html",context)


def addtocart(request,pid):
    context={}
    if request.user.is_authenticated:
        u=User.objects.filter(id=request.user.id)
        p=product.objects.filter(id=pid)
        productss=product.objects.all()

        q1=Q(userid=u[0])
        q2=Q(pid=p[0])
        c=Cart.objects.filter(q1&q2)
        n=len(c)
        context["products"]=p
        context["productss"]=productss
        if n==1:
            context['msg']="Product is already exist"
            return render(request,"product_details.html",context)
        else:
            cart=Cart.objects.create(pid=p[0],userid=u[0])
            cart.save()
            context['msg']="Product added in cart successful !"
            return render (request,"product_details.html",context)

    else:

        return redirect("/login")
    
    return render (request,"product_details.html",context)
    

def view_cart(request):
    context={}
    if request.user.is_authenticated:
        c=Cart.objects.filter(userid=request.user.id)
        context["carts"]=c
        totallyqty=0
        totallprice=0

    
        for i in c:
            totallyqty=totallyqty+i.qty
            totallprice=totallprice+100+i.qty*i.pid.price
        context["items"]=totallyqty
        context["totallprice"]=totallprice
        return render(request,"view_cart.html",context)
    else:
        return redirect("/login")

def updateqty(request,x,cid):
    c=Cart.objects.filter(id=cid)
    q=c[0].qty 
    if x=="1":
        q=q+1
    elif q>1:
        q=q-1
    c.update(qty=q)

   
    return redirect("/view_cart") 


def removecart(request,cid):
    context={}
    c=Cart.objects.filter(id=cid)
    c.delete()
    context['msg']="Product remove from cart"
    c=Cart.objects.filter(userid=request.user.id)
    
    context["carts"]=c
    return render(request,"view_cart.html",context)

def search(request):

    query=request.GET['query']
    products= product.objects.filter(pname__icontains=query)
    productss=product.objects.all()
    context={'products': products,
   'productss': productss }
    return render(request, 'search.html', context)

def about(request):
    return render(request,"about.html")


def contact(request):
    return render(request,"contact.html")


import random

def placeorder(request):
    c=Cart.objects.filter(userid=request.user.id)
    
    oid=random.randint(11111,99999)
    for x in c:
        amount=x.qty*x.pid.price
        o=Order.objects.create(order_id=oid,amt=amount,p_id=x.pid,user_id=x.userid)
        o.save()
    return redirect("/fetchorder")


def fetchorder(request):
    context={}
    orders=Order.objects.filter(user_id=request.user.id)
    c=Cart.objects.filter(userid=request.user.id)
    context["carts"]=c
    context["orders"]=orders
    sum=0
    n=len(orders)
    for order in orders:
        sum=sum+100+order.amt
    context["total"]=sum
    
    return render (request,"placeorder.html",context)
    

def makepayment(request):
    client = razorpay.Client(auth=("rzp_test_I7C0Tt7if7jjRS", "jlibpy1HmtPz4Foe9Sjaky1o"))
    orders=Order.objects.filter(user_id=request.user.id)
    context={}
    context["orders"]=orders
    sum=0
    for x in orders:
        sum=sum+x.amt+100
        orderid=x.order_id

    data = { "amount": sum*100, "currency": "INR", "receipt": orderid }
    payment = client.order.create(data=data)
  
    context={}
    context["payment"]=payment
    return render(request,"pay.html",context)
    
def paymantsuccess(request):
    return HttpResponse("payment Success")




