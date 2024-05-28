from django.http.response import JsonResponse
from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.contrib import messages
from store.models import Product, Cart
from django.contrib.auth.decorators import login_required


def addtocart(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            product_check = Product.objects.filter(id=prod_id).first()
            print(request.user.id)

            if (product_check):
                try:
                    prod_qty = int(request.POST.get('product_qty'))
                except Exception as e:
                    prod_qty = 1

                cart_entry = Cart.objects.filter(user=request.user, product_id=prod_id).first()

                if cart_entry:  # If the product is already in the cart
                    new_qty = cart_entry.product_qty + prod_qty
                    if product_check.quantity >= new_qty:  # Check if the total quantity is available
                        cart_entry.product_qty = new_qty
                        cart_entry.save()
                        return JsonResponse({'status': "Product quantity updated in the cart"})
                    else:
                        return JsonResponse({'status': f"Only {product_check.quantity} quantity available"})

                else:
                    if product_check.quantity >= prod_qty:
                        Cart.objects.create(user=request.user, product_id=prod_id, product_qty=prod_qty)
                        return JsonResponse({'status': "Product added successfully"})
                    else:
                        return JsonResponse({'status': "Only" + str(product_check.quantity) + "quantity available"})
            else:
                return JsonResponse({'status': "No such product found"})
        else:
            return JsonResponse({'status': "Login to Continue"})
    return redirect('/')


@login_required(login_url='loginpage')
def viewcart(request):
    cart = Cart.objects.filter(user=request.user)
    for i in cart:
        print(i.product.selling_price)
    context = {'cart': cart, 'total_item': cart.count()}
    print(context)
    return render(request, "cart.html", context)


def updatecart(request):
    if request.method == "POST":
        prod_id = int(request.POST.get('product_id'))
        input_product_qty = int(request.POST.get('product_qty'))
        prod_qty = Product.objects.get(id=prod_id)
        total_prod_quantity = prod_qty.quantity

        # if (Cart.objects.filter(user=request.user, product_id=prod_id)):
        if total_prod_quantity > input_product_qty:
            print(total_prod_quantity)
            print(input_product_qty)
            cart, created = Cart.objects.get_or_create(user=request.user, product_id=prod_id)
            cart.product_qty = input_product_qty
            cart.save()
            prod_qty = int(request.POST.get('product_qty'))
            cart = Cart.objects.get(product_id=prod_id, user=request.user)
            cart.product_qty = prod_qty
            cart.save()
            return JsonResponse({'status': "Updated Successfully"}, status=200)
        else:
            return JsonResponse({'status': "Out of Stock"}, status=400)
    return redirect('/')


def deletecartitem(request):
    if request.method == "POST":
        prod_id = int(request.POST.get('product_id'))
        if (Cart.objects.filter(user=request.user, product_id=prod_id)):
            cartitem = Cart.objects.filter(product_id=prod_id, user=request.user)
            print(cartitem)
            cartitem.delete()
            return JsonResponse({'status': "Deleted Successfully"})
    return redirect('/')

# def productview(request, cate_slug, prod_slug):
#     if request.method == 'POST':
#         if (Category.objects.filter(slug=cate_slug, status=0)):
#             if (Product.objects.filter(slug=prod_slug, status=0)):
#                 products = Product.objects.filter(slug=prod_slug, status=0).first()
#                 print(products)
#                 cart = Cart.objects.filter(user=request.user)
#                 context = {"products": products, 'total_item': cart.count()}
#
#         rate = request.POST.get('rating')
#         comment = request.POST.get('review')
#         products = Product.objects.filter(slug=prod_slug).first()
#         print("products::::::",products)
#         data = Review(user=request.user, product=products, rate=rate, comment=comment)
#         data.save()
#         return render(request, "view.html", context)
#
#     else:
#         if (Category.objects.filter(slug=cate_slug, status=0)):
#             if (Product.objects.filter(slug=prod_slug, status=0)):
#                 products = Product.objects.filter(slug=prod_slug, status=0).first()
#                 print(products)
#
#                 cart = Cart.objects.filter(user=request.user)
#                 context = {"products": products, 'total_item': cart.count()}
#             else:
#                 messages.error(request, 'no such product found')
#                 return redirect('/')
#         else:
#             messages.error(request, 'no such category found')
#             return redirect('/')
#         return render(request, "view.html", context)
