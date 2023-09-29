from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render
from django.views.generic import DetailView, TemplateView

from product.models import Product, Category, Comment


def detail(request, id):
    product = Product.objects.get(id=id)
    if request.method == 'POST':
        body = request.POST.get('message')
        Comment.objects.create(body=body, product=product, user=request.user)
    return render(request, 'product/product_detail.html', {'product': product})


def detall_all(request):
    product = Product.objects.all()
    return render(request, 'product/product_detail.html', {'product': product})


def category_product(request):
    category = Category.objects.all()
    # category_1 = Category.objects.get(id=category.get('slug'))
    # articles = category.article_set.all()
    return render(request, 'includes/navbar.html', {'categories': category})


def category_test(request):
    category = Category.objects.all()
    return render(request, 'category.html', {'categories': category})


# class NavbarPartialView(TemplateView):
#     template_name = 'base.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(NavbarPartialView, self).get_context_data()
#         context['categories'] = Category.objects.all()
#         return context

def product_list(request):
    product = Product.objects.all()
    categories = Category.objects.all()
    categoryss = []
    for catts in categories:
        if not catts.parent:
            if catts.catt.all():
                categoryss.append(catts)
    color = request.GET.getlist('color')
    size = request.GET.getlist('size')
    cat = request.GET.getlist('cat')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    q = request.GET.get('q')

    test = []

    if color:
        product = product.filter(color__title__in=color).distinct()
        test.append(color)
    if size:
        product = product.filter(size__title__in=size).distinct()
        test.append(size)
    if request.GET.get('next'):
        cat_2 = request.GET.getlist('next')
        product = product.filter(category__title__in=cat_2).distinct()
    if cat:
        print("yes")
        product = product.filter(category__title__in=cat).distinct()
        test.append(cat)
    # print(name)
    if min_price and max_price:
        product = product.filter(price__gte=min_price, price__lte=max_price).distinct()
        test.append(min_price)
        test.append(max_price)

    if q:
        product = product.filter(title__icontains=q).distinct()
    print(q)
    pagenumber = request.GET.get('page')
    paginator = Paginator(product, 1)
    pp = paginator.get_page(pagenumber)

    return render(request, 'product/product_list.html', {'products': pp, 'categories': categoryss, 'test': test})
