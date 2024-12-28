
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from store.models import ProductType
from store.models import Requests, ItemRequest
from store.utils import utils


class DispatchLoginRequiredMixin(View):
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('store:profile_create')

        return super().dispatch(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)  # type: ignore
        qs = qs.filter(user=self.request.user)
        return qs


# Create your views here.

class RequestPay(DispatchLoginRequiredMixin, DetailView):
    template_name = 'store/request/pay.html'
    model = Requests
    pk_url_kwarg = 'pk'
    context_object_name = 'request'


class RequestSave(View):

    template_name = 'store/request/pay.html'

    def get(self, *args, **kwargs):
        # get cart
        cart = self.request.session.get('cart')
        # messages
        msg_error_no_stock = ''

        if not self.request.user.is_authenticated:
            messages.error(
                self.request,
                'You need to login',
            )
            return redirect('store:profile_create')

        if not cart:
            messages.error(
                self.request,
                'Cart is empty!',
            )
            return redirect('store:list')

        cart_ProductTypes_ids = [v for v in cart]

        bd_ProductTypes = list(
            ProductType.objects.select_related('product')
            .filter(id__in=cart_ProductTypes_ids)
        )

        for pT in bd_ProductTypes:
            _id = str(pT.pk)
            stock = pT.stock

            cart_qty = cart[_id]['qty']
            unit_price = cart[_id]['unit_price']
            promo_price = cart[_id]['promo_price']

            if stock < cart_qty:
                cart[_id]['qty'] = stock
                cart[_id]['qty_price'] = stock * unit_price
                cart[_id]['qty_promo_price'] = stock * promo_price

                msg_error_no_stock = ('Not enougth stock for some products, '
                                      'quantity adjusted to stock available, '
                                      'please check your cart'
                                      )

            if msg_error_no_stock:
                messages.error(
                    self.request,
                    msg_error_no_stock,
                )
                self.request.session.save()

                return redirect('store:cart')

        cart_total_qty = utils.cart_total_qtd(cart)
        cart_total_value = utils.cart_total(cart)

        request = Requests(
            user=self.request.user,
            total=cart_total_value,
            qtd_total=cart_total_qty,
            status='C',
        )

        request.save()

        ItemRequest.objects.bulk_create(
            [
                ItemRequest(
                    request=request,
                    product=item['product_name'],
                    product_id=item['product_id'],
                    productType=item['pType_name'],
                    productType_id=item['pType_id'],
                    price=item['qty_price'],
                    promo_price=item['qty_promo_price'],
                    quantity=item['qty'],
                    image=item['image'],
                )for item in cart.values()
            ]
        )

        # context = {}

        # return render(
        #     self.request,
        #     self.template_name,
        #     context,
        # )

        del self.request.session['cart']
        return redirect(
            reverse(
                'store:request_pay',
                kwargs={
                    'pk': request.pk,
                }
            )
        )


class RequestList(DispatchLoginRequiredMixin, ListView):
    model = Requests
    context_object_name = 'requests'
    template_name = 'store/request/list.html'
    paginate_by = 5
    ordering = ['-id']


class RequestDetail(DispatchLoginRequiredMixin, DetailView):
    model = Requests
    context_object_name = 'request'
    template_name = 'store/request/detail.html'
    pk_url_kwarg = 'id'
