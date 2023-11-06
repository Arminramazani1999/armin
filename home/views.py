from django.shortcuts import render
from product.models import Product, Category


def home(request):
    product = Product.objects.all()
    categories = Category.objects.all()
    recent_product = Product.objects.all()[:4]
    product_views = []
    product_views_2 = []
    for i in product:
        product_views.append(i.review)
    product_views.sort()
    product_views.reverse()
    sum = 0
    s = 0
    for i in product_views[0:4]:
        product_filters_views = Product.objects.filter(review=i)
        for j in product_filters_views:
            if j not in product_views_2:
                print(j)
                product_views_2.append(j)
                sum += 1
                if sum == 4:
                    s = 1
                    break
        if s == 1:
            break

    return render(request, 'home/home.html',
                  {'products': product, 'categories': categories, 'recents': recent_product,
                   'product_filters_views': product_views_2})
