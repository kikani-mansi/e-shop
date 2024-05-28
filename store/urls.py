from django.urls import path
from .views import *
from .authview import *
from .cart import *
from .wishlist import *
from .checkout import *
from .order import *


urlpatterns = [
    path("",home,name="home"),
    path('collections',collections,name="collections"),
    path('collections/<str:slug>',collectionsview,name="collectionsview"),
    path('collections/<str:cate_slug>/<str:prod_slug>',productview,name="productview"),
    path('register/',register,name="register"),
    path('login/',loginpage,name="login"),
    path('logout/',logoutpage,name="logout"),
    path("add-to-cart",addtocart,name="addtocart"),
    path("cart",viewcart,name="cart"),
    path("update-cart",updatecart,name="updatecart"),
    path("delete-cart-item",deletecartitem,name="deletecartitem"),
    path("wishlist",index,name="wishlist"),
    path("add-to-wishlist",addtowishlist,name="addtowishlist"),
    path("delete-wishlist-item",deletewishlistitem,name="deletewishlistitem"),
    path('checkout',index1,name="checkout"),
    path('place-order',placeorder,name="placeorder"),
    path('proceed-to-pay',razorpaycheck,name="razorpaycheck"),
    path('my-orders',index2,name="myorders"),
    path('product-list',productlistAjax),
    path('searchproduct',searchproduct,name="searchproduct"),
    path('view-order/<str:t_no>',vieworder,name="orderview"),





]