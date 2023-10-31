from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render
from django.views.generic import DetailView, TemplateView

from cart.cart_module import Cart
from product.filters import ProductFilter
from product.models import Product, Category, Comment


def detail(request, id):
    products = Product.objects.all()
    product = Product.objects.get(id=id)
    product.review += 1
    product.save()
    if request.method == 'POST':
        body = request.POST.get('message')
        Comment.objects.create(body=body, product=product, user=request.user)
    return render(request, 'product/product_detail.html', {'product': product, 'prodoucts': products})


def detall_all(request):
    product = Product.objects.all()
    return render(request, 'product/product_detail.html', {'product': product})


def category_product(request):
    category = Category.objects.all()
    cart = Cart(request)
    # quantity = 0
    # if request.session.get('number') is not None:
    #     print('================================yes===================')
    #     quantity = request.session.get('number')
    # # category_1 = Category.objects.get(id=category.get('slug'))
    # # articles = category.article_set.all()
    # if quantity == 0:
    #     context = {'categories': category}
    # else:
    #     context = {'categories': category, 'quantity': quantity,}

    return render(request, 'includes/navbar.html', {'categories': category, 'cart': cart})


def category_test(request):
    category = Category.objects.all()
    return render(request, 'category.html', {'categories': category})


# def product_list(request):
#     context = {}
#
#     filtered_product = ProductFilter(
#         request.GET,
#         queryset=Product.objects.all()
#     )
#     context['filtered_product'] = filtered_product
#     return render(request, 'product/product_list.html', context=context)
#
#
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
    next_page = request.GET.getlist('next')

    if color:
        product = product.filter(color__title__in=color).distinct()
    if size:
        product = product.filter(size__title__in=size).distinct()
    if next_page:
        product = product.filter(category__title__in=next_page).distinct()
    if cat:
        product = product.filter(category__title__in=cat).distinct()
    if min_price and max_price:
        product = product.filter(price__gte=min_price, price__lte=max_price).distinct()
    if q:
        product = product.filter(title__icontains=q).distinct()
    page_number = request.GET.get('page')
    paginator = Paginator(product, 1)
    object_list = paginator.get_page(page_number)

    return render(request, 'product/product_list.html', {'products': object_list, 'categories': categoryss})
