from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic import DetailView, TemplateView

from product.models import Product, Category, Comment


def detail(request, id):
    product = Product.objects.get(id=id)
    if request.method == 'POST':
        body = request.POST.get('message')
        Comment.objects.create(body=body, product=product, user=request.user)
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
    color = request.GET.getlist('color')
    size = request.GET.getlist('size')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    print(color, size, min_price, max_price)
    if color:
        product = product.filter(color__title__in=color).distinct()
    if size:
        product = product.filter(size__title__in=size).distinct()
    if min_price and max_price:
        product = product.filter(price__gte=min_price, price__lte=max_price).distinct()

    pagenumber = request.GET.get('page')
    paginator = Paginator(product, 1)
    product = paginator.get_page(pagenumber)

    return render(request, 'product/product_list.html', {'products': product})
