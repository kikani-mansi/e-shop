from django.http.response import JsonResponse
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *

@login_required(login_url='loginpage')
def index(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    context = {'wishlist':wishlist}
    print(wishlist)
    return render(request,'wishlist.html',context)

def addtowishlist(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            product_check = Product.objects.get(id=prod_id)
            if (product_check):
                if (Wishlist.objects.filter(user=request.user, product_id=prod_id)):
                    return JsonResponse({'status': "Product Already in Wishlist"})
                else:
                    Wishlist.objects.create(user=request.user, product_id=prod_id)
                    return JsonResponse({'status': "Product added to Wishlist"})

            else:
                return JsonResponse({'status': "No such product found"})
        else:
            return JsonResponse({'status': "Login to Continue"})
    return redirect('/')

def deletewishlistitem(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))

            if (Wishlist.objects.filter(user=request.user, product_id=prod_id)):
                wishlistitem = Wishlist.objects.filter(product_id=prod_id, user=request.user)
                wishlistitem.delete()
                print(wishlistitem)
                return JsonResponse({'status': "Product remove from Wishlist"})
            else:
                return JsonResponse({'status': "Product not found in Wishlist"})

        else:
            return JsonResponse({'status': "Login to Continue"})

    return redirect('/')
