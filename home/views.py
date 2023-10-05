from django.shortcuts import render
from product.models import Product, Category


def home(request):
    product = Product.objects.all()
    categories = Category.objects.all()
    recent_product = Product.objects.all()[:4]
    # sum = []
    # n = int(request.session.get('number'))
    # sum.append(n)
    # print(sum)
    return render(request, 'home/home.html',
                  {'products': product, 'categories': categories, 'recents': recent_product})
