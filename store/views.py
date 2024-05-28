import json

from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.http.response import JsonResponse



# Create your views here.
def home(request):
    category = Category.objects.filter(status=0)
    if request.user.id is not None:
        cart = Cart.objects.filter(user=request.user)
        # print(request.user)
        # if request.user != AnonymousUser:
        #     cart = Cart.objects.filter(user=request.user)
        #     total_item = cart.count()
        # else:
        #     total_item = 0
        context = {'category': category, 'total_item': cart.count()}
        return render(request, "index.html", context)
    else:
        return redirect('/login')


def collections(request):
    category = Category.objects.filter(status=0)
    context = {'category': category}
    return render(request, "Collections.html", context)


def collectionsview(request,slug):
    if (Category.objects.filter(slug=slug, status=0)):
        products = Product.objects.filter(category__slug=slug)
        category_name = Category.objects.filter(slug=slug).first()
        cart = Cart.objects.filter(user=request.user)
        context = {"products": products, "category": category_name, 'total_item': cart.count()}
        return render(request, "index1.html", context)
    else:
        messages.warning(request, 'no such category found')
        return redirect('/')


def productview(request, cate_slug, prod_slug):
    if request.method == 'POST':
        if (Category.objects.filter(slug=cate_slug, status=0)):
            if (Product.objects.filter(slug=prod_slug, status=0)):
                products = Product.objects.filter(slug=prod_slug, status=0).first()
                # print(products)
                cart = Cart.objects.filter(user=request.user)
                context = {"products": products, 'total_item': cart.count()}

        rate = request.POST.get('rating')
        # print(rate)
        comment = request.POST.get('review')
        products = Product.objects.filter(slug=prod_slug).first()
        # print("products::::::",products)
        data = Review(user=request.user, product=products, rate=rate, comment=comment)
        data.save()
        messages.success(request, "Review Added Successfully")
        return redirect('/')

    else:
        if (Category.objects.filter(slug=cate_slug, status=0)):
            if (Product.objects.filter(slug=prod_slug, status=0)):
                products = Product.objects.filter(slug=prod_slug, status=0).first()
                # print(products)
                review = Review.objects.filter(product=products)
                ratings = []

                for rev in review:
                    ratings.append(rev.rate)
                for rating in ratings:
                    print(rating)


                a = ratings.count(1)
                b = ratings.count(2)
                c = ratings.count(3)
                d = ratings.count(4)
                e = ratings.count(5)


                star_rating = {"1star":a, "2star":b, "3star":c, "4star":d, "5star":e}
                star_rating_list = [star_rating]

                list=[]
                for lists in a,b,c,d,e:
                    list.append(lists)
                rating_sum = sum(list)

                if rating_sum:

                    a_per = int(a / rating_sum *100)
                    b_per = int(b / rating_sum *100)
                    c_per = int(c / rating_sum *100)
                    d_per = int(d / rating_sum *100)
                    e_per = int(e / rating_sum *100)
                    average_rating = round(sum(ratings) / len(ratings), 1)
                else:
                    a_per = 0
                    b_per = 0
                    c_per = 0
                    d_per = 0
                    e_per = 0
                    average_rating = 0

                star_per = {"1star":a_per, "2star":b_per, "3star":c_per, "4star":d_per, "5star":e_per}
                star_per_list = [star_per]
                print(star_per_list)

                cart = Cart.objects.filter(user=request.user)
                context = {"products": products,"review":review,"star_rating_list":star_rating_list,"average_rating":average_rating,"star_per_list":star_per_list, 'total_item': cart.count()}
            else:
                messages.error(request, 'no such product found')
                return redirect('/')
        else:
            messages.error(request, 'no such category found')
            return redirect('/')
        return render(request, "view.html", context)

def productlistAjax(request):
    categorys = Category.objects.filter(status=0).values_list('name',flat=True)
    categorysList = list(categorys)

    return JsonResponse(categorysList,safe=False)

def searchproduct(request):
    if request.method == "POST":
        searchedterm = request.POST.get('productsearch')
        if searchedterm == "":
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            product = Category.objects.filter(name__contains=searchedterm).first()
            if product:
                return redirect('collections/'+product.slug)
            else:
                messages.info(request, "No product matched your search")
                return redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))









