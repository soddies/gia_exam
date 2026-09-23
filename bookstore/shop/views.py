from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Product, Category, Manufacturer
from django.db.models import Q

def login_views(request):
    if request.session.get('is_authenticated'):
        return redirect('main')

    if request.method == 'POST':
        login_input = request.POST.get('login', '').strip()
        password_input = request.POST.get('password', '').strip()

        user = User.objects.filter(login=login_input, password=password_input).first()

        if user:
            request.session['is_authenticated'] = True
            request.session['user_id'] = user.user_id
            request.session['user_fullname'] = user.full_name
            request.session['role'] = user.role_id.role_user
            request.session['role_id'] = user.role_id.role_id
            return redirect('main')
        else:
            return render(request, 'login.html', {'error': 'Неверный логин или пароль'})

    return render(request, 'login.html')

def main_view(request):
    if not request.session.get('is_authenticated'):
        return redirect('login')

    user = User.objects.get(user_id=request.session['user_id'])
    role_name = request.session.get('role', '')

    products = Product.objects.all()

    if role_name in ['Администратор', 'Менеджер']:
        search_query = request.GET.get('search', '')
        if search_query:
            products = products.filter(
                Q(product_name__icontains=search_query) | Q(article__icontains=search_query))

        category_filter = request.GET.get('category', '')
        if category_filter:
            products = products.filter(category_id=category_filter)

        manufacturer_filter = request.GET.get('manufacturer', '')
        if manufacturer_filter:
            products = products.filter(manufacturer_id=manufacturer_filter)

        sort_by = request.GET.get('sort', 'product_name')
        if sort_by in ['product_name', 'price', 'article']:
            products = products.order_by(sort_by)

        categories = Category.objects.all()
        manufacturers = Manufacturer.objects.all()

        context = {
            'user': user,
            'products': products,
            'role': role_name,
            'categories': categories,
            'manufacturers': manufacturers,
            'search_query': search_query,
            'selected_category': category_filter,
            'selected_manufacturer': manufacturer_filter,
            'selected_sort': sort_by,
        }

    else:
        context = {
            'user': user,
            'role': role_name,
            'products': products
        }

    return render(request, 'main.html', context)

def logout_view(request):
    request.session.flush()
    return redirect('login')

def product_create(request):
    if not request.session.get('is_authenticated'):
        return redirect('login')

    if request.session.get('role') != 'Администратор':
        return redirect('main')

    if request.method == 'POST':
        Product.objects.create(
            article=request.POST.get('article'),
            product_name=request.POST.get('product_name'),
            unit_id=request.POST.get('unit_id'),
            price=request.POST.get('price'),
            manufacturer_id=request.POST.get('manufacturer_id'),
            supplier_id=request.POST.get('supplier_id'),
            category_id=request.POST.get('category_id'),
            discount=request.POST.get('discount',0),
            stock_quantity=request.POST.get('stock_quantity',0),
            description=request.POST.get('description',''),
            image_path=request.POST.get('image_path', ''),
        )
        return redirect('main')

    return render(request, 'product_form.html', {'action': 'create'})

def product_update(request, product_id):
    if not request.session.get('is_authenticated'):
        return redirect('login')

    if request.session.get('role') != 'Администратор':
        return redirect('main')

    product = get_object_or_404(Product, product_id=product_id)
    if request.method == 'POST':
        product.article = request.POST.get('article')
        product.product_name = request.POST.get('product_name')
        product.unit_id = request.POST.get('unit_id')
        product.price = request.POST.get('price')
        product.manufacturer_id = request.POST.get('manufacturer_id')
        product.supplier_id = request.POST.get('supplier_id')
        product.discount = request.POST.get('discount', 0)
        product.stock_quantity = request.POST.get('stock_quantity', 0)
        product.description = request.POST.get('description', '')
        product.image_path = request.POST.get('image_path', '')
        product.save()
        return redirect('main')

    return render(request, 'product_form.html', {'product': product, 'action': 'update'})

def product_delete(request, product_id):
    if not request.session.get('is_authenticated'):
        return redirect('login')

    if request.session.get('role') != 'Администратор':
        return redirect('main')

    product = get_object_or_404(Product, product_id=product_id)

    if request.method == 'POST':
        product.delete()
        return redirect('main')

    return render(request, 'product_delete.html', {'product': product, 'action': 'delete'})


# Create your views here.
