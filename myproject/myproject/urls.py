"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/',views.index),
    path('contact/',views.contact),
    path('register/',views.register),
    path('login/',views.login),
    path('logout/',views.ulogout),
    path('change_pass/',views.change_pass,name='changepass'),
    path('shopbycategory/<cid>/',views.shopbycategory),
    path('filterbycategory/<cid>/',views.filterbycategory),
    path('sortbyprice/<s>/',views.sortbyprice),
    path('filterbyprice/',views.filterbyprice),

    path('product_details/<pid>/',views.product_details),
    path('addtocart/<pid>/',views.addtocart),
    path('view_cart/',views.view_cart),
    path('updateqty/<x>/<cid>/',views.updateqty),
    path('removecart/<cid>/',views.removecart),
    path('search/',views.search),
    path('about/',views.about),
    path('contact/',views.contact),
    path('placeorder/',views.placeorder),
    path('fetchorder/',views.fetchorder),
    path('makepayment/',views.makepayment),
    path('pay/',views.paymantsuccess)


]
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

