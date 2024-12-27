
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from store.models import Product, ProductType, UserProfile
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.views import View
from django.db.models import Q


# to debug
from pprint import pprint

# Create your views here.


class ProductList(ListView):
    """Class representing a Product"""
    model = Product
    template_name = 'store/product/list.html'
    context_object_name = 'products'
    paginate_by = 6
    ordering = ['-id']


class ProductDetail(DetailView):
    model = Product
    template_name = 'store/product/detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'


class AddToCart(View):
    def get(self, *args, **kwargs):
        # get product variation id
        pType_id = self.request.GET.get('pType_id')
        # if product variation not exist set error message and return to home
        if not pType_id:
            messages.error(
                self.request,
                'Product not found!',
            )
            return redirect(reverse('store:list'))
        # get product ( product variation) to add to cart
        pType_to_add = get_object_or_404(ProductType, id=pType_id)
        # get product
        _product = pType_to_add.product
        _product_id = _product.id  # type: ignore
        _product_name = _product.name
        _pType_name = pType_to_add.name or ''
        _pType_id = pType_id
        _unit_price = pType_to_add.price
        _unit_promo_price = pType_to_add.promo_price
        _qty = 1
        _slug = _product.slug
        _image = _product.image
        _pType_stock = pType_to_add.stock

        if _image:
            _image = _image.name
        else:
            _image = ''

        # check stock
        if _pType_stock < 1:
            messages.error(
                self.request,
                'Out of stock'
            )
            return redirect(reverse('store:list'))

        # check if cart exist, if not save one
        if not self.request.session.get('cart'):
            self.request.session['cart'] = {}
            self.request.session.save()
        # get cart, new or existing
        cart = self.request.session['cart']

        if pType_id in cart:
            # product exist in cart
            # check unit in cart
            qty_in_cart = cart[pType_id]['qty']
            # add one more unit to cart
            qty_in_cart += 1
            # check if it available one more
            if _pType_stock < qty_in_cart:
                messages.warning(
                    self.request,
                    f'No stock available for {qty_in_cart}x of '
                    f'"{_product_name}", {_pType_stock} available in cart'
                )
                qty_in_cart = _pType_stock
                # return
                return redirect(self.request.META['HTTP_REFERER'])

            # update cart
            # set cart qty
            cart[_pType_id]['qty'] = qty_in_cart
            # set cart total price
            cart[_pType_id]['qty_price'] = _unit_price * qty_in_cart
            # set cart total price
            cart[_pType_id]['qty_promo_price'] = _unit_promo_price * qty_in_cart

        else:
            # product does not exist in cart, add it
            cart[pType_id] = {
                'product_id': _product_id,
                'product_name': _product_name,
                'pType_name': _pType_name,
                'pType_id': _pType_id,
                'unit_price': _unit_price,
                'promo_price': _unit_promo_price,
                'qty_price': _unit_price,
                'qty_promo_price': _unit_promo_price,
                'qty': _qty,
                'slug': _slug,
                'image': _image,
            }

        # check if product is Simple or has Variations
        if pType_to_add.product.p_type == 'S':
            _message = f'{_product_name} added to your cart'
        else:
            _message = f'{_product_name} type {_pType_name} added to your cart'

        messages.success(
            self.request,
            _message
        )

        # save cart in session
        self.request.session.save()

        return redirect(self.request.META['HTTP_REFERER'])


class RemoveFromCart(View):
    def get(self, *args, **kwargs):
        pType_id = self.request.GET.get('id')
        #
        _cart = self.request.session.get('cart')

        if not pType_id or not _cart or not pType_id in _cart:
            messages.error(
                self.request,
                'Product not found!',
            )
            return redirect(reverse('store:list'))

        # remove from cart
        del _cart[pType_id]
        # save
        self.request.session.save()
        # success
        messages.success(
            self.request,
            'Product removed from cart',
        )

        return redirect(self.request.META['HTTP_REFERER'])


class Cart(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'store/product/cart.html')


class Resume(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('store:profile_create')

        profile = UserProfile.objects.get(user=self.request.user)
        # check if profile exists
        if not profile:
            messages.error(
                self.request,
                'Please update your profile'
            )
            return redirect('store:profile_create')

        # check cart
        if not self.request.session.get('cart'):
            messages.error(
                self.request,
                'Please add products to your cart'
            )
            return redirect('store:list')

        context = {
            'user': self.request.user,
            'profile': profile,
            'cart': self.request.session['cart'],
        }

        return render(self.request, 'store/product/resume.html', context)


class ProductSearch(ProductList):
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)

        _term = self.request.GET.get('term') or self.request.session['_term']

        if _term:
            qs = Product.objects.filter(
                Q(name__icontains=_term) |
                Q(short_description__icontains=_term) |
                Q(description__icontains=_term)
            )
            self.request.session['_term'] = _term
            self.request.session.save()

        return qs
