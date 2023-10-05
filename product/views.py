from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render
from django.views.generic import DetailView, TemplateView

from product.models import Product, Category, Comment


def detail(request, id):
    products = Product.objects.all()
    product = Product.objects.get(id=id)
    if request.method == 'POST':
        body = request.POST.get('message')
        Comment.objects.create(body=body, product=product, user=request.user)
    return render(request, 'product/product_detail.html', {'product': product, 'prodoucts': products})


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
    cat = request.GET.get('cat')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    q = request.GET.get('q')
    next_page = request.GET.getlist('next')

    test = ['color', 'size', 'cat', 'q', 'next']
    if color:
        product = product.filter(color__title__in=color).distinct()
        # for i in color:
        #     test.append(i)

    if size:
        product = product.filter(size__title__in=size).distinct()
        # for i in size:
        #     test.append(i)
    if next_page:
        # cat_2 = request.GET.getlist('next')
        product = product.filter(category__title__in=next_page).distinct()
        # for i in next_page:
        #     test.append(i)
    if cat:
        product = product.filter(category__title__in=cat).distinct()
        # for i in cat:
        #     test.append(i)
    # print(name)
    if min_price and max_price:
        product = product.filter(price__gte=min_price, price__lte=max_price).distinct()
        test.append(min_price)
        test.append(max_price)

    if q:
        product = product.filter(title__icontains=q).distinct()
        # test.append(q)
    for i in test:
        print(request.GET.get(i))
    pagenumber = request.GET.get('page')
    paginator = Paginator(product, 1)
    pp = paginator.get_page(pagenumber)

    return render(request, 'product/product_list.html', {'products': pp, 'categories': categoryss, 'test': test})
