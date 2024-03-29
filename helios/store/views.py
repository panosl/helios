# -*- coding: utf-8 -*-
from __future__ import with_statement
from decimal import Decimal
from importlib import import_module

from django.contrib.auth.decorators import login_required
from django.core.exceptions import FieldError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView, ListView
from helios.conf import settings
from helios.store.decorators import cart_required
from helios.store.models import Category, Collection, Product


module_name, model_name = settings.PRODUCT_MODEL.rsplit('.', 1)
ProductModel = getattr(import_module(module_name), model_name)
cart = getattr(import_module(settings.CART), 'cart')


class ProductDetail(DetailView):
    context_object_name = model_name.lower()
    queryset = ProductModel.objects.all()
    model = ProductModel
    template_name = 'store/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data(**kwargs)
        try:
            context['category'] = self.get_object().category
        except AttributeError:
            pass
        return context


def cart_debug(request):
    return HttpResponse('%s' % request.session.items())


def cart_clear(request):
    with cart(request) as session_cart:
        session_cart.clear()
    return HttpResponse('Done')


def cart_set_quantity(request, product_id, success_url='/store/cart'):
    if not request.method == 'POST':
        return HttpResponseRedirect(success_url)

    try:
        quantity = int(request.POST.get('quantity'))
    except ValueError:
        return HttpResponseRedirect(success_url)

    product_id = int(product_id)
    with cart(request) as session_cart:
        try:
            items_in_stock = session_cart[product_id].product.stock

            if quantity < 0:
                return HttpResponseRedirect(success_url)
            elif quantity == 0 or items_in_stock == 0:
                del session_cart[product_id]
            else:
                if quantity >= items_in_stock:
                    session_cart[product_id]['quantity'] = items_in_stock
                else:
                    session_cart[product_id]['quantity'] = quantity
        except AttributeError:
            if quantity < 0:
                return HttpResponseRedirect(success_url)
            elif quantity == 0:
                del session_cart[product_id]
            else:
                session_cart[product_id]['quantity'] = quantity

    return HttpResponseRedirect(success_url)


def product_add(request, slug=''):
    try:
        product = ProductModel.objects.get(slug=slug)
    except ProductModel.DoesNotExist:
        return HttpResponse('That product does not exist.')

    with cart(request) as session_cart:
        session_cart.add_product(product.id, 1)

    if request.is_ajax():
        with cart(request) as session_cart:
            return HttpResponse(str(session_cart.get_product_count()))

    url = request.META.get('HTTP_REFERER', None)
    if url is None:
        url = reverse('store_product_list')

    return HttpResponseRedirect(url)


def product_remove(request, slug=''):
    try:
        product = ProductModel.objects.get(slug=slug)
    except ProductModel.DoesNotExist:
        return HttpResponse('That product does not exist.')

    with cart(request) as session_cart:
        try:
            session_cart.remove_product(product.id)
        except KeyError:
            return HttpResponse('Does not have one of those!')

    return HttpResponseRedirect(reverse('store_cart'))


# def category_list(request, category, **kwargs):
# category = get_object_or_404(Category, slug=category)
##TODO include the category along with the children

# fieldname = request.GET.get('sort', None)
# print request.GET.get('sort', None)
# print fieldname

# if category.is_root_node():
# product_list = Product.objects.filter(category__slug__in=(c.slug for c in category.get_children())) | Product.objects.filter(category__slug__exact=category.slug)
# else:
# product_list = Product.objects.filter(category__slug__exact=category.slug)
# kwargs['extra_context']['category'] = category

# try:
# product_list = product_list.order_by(fieldname)
# kwargs['extra_context']['sorting'] = fieldname
# except TypeError:
# pass
# except FieldError:
# pass

# return object_list(request, queryset=product_list, **kwargs)


class ProductList(ListView):
    model = Product
    context_object_name = 'product_list'

    def get_queryset(self):
        self.sort_by = self.request.GET.get('sort')
        if not self.sort_by in ['last_modified', 'slug', 'base_price']:
            self.sort_by = None
        self.category = get_object_or_404(Category, slug=self.kwargs['category'])

        if self.category.is_root_node():
            queryset = Product.objects.filter(
                category__slug__in=(c.slug for c in self.category.get_children())
            ) | Product.objects.filter(category__slug__exact=self.category.slug)
        else:
            queryset = Product.objects.filter(category=self.category)

        # queryset = Product.objects.filter(category=self.category)

        if self.sort_by:
            return queryset.order_by(self.sort_by)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ProductList, self).get_context_data(**kwargs)
        context['category'] = self.category
        context['sort_by'] = self.sort_by
        return context


class CollectionList(ListView):
    model = Collection
    context_object_name = 'product_list'

    def get_queryset(self):
        self.collection = get_object_or_404(Collection, slug=self.kwargs['collection'])

        return self.collection.products.all()

    def get_context_data(self, **kwargs):
        context = super(CollectionList, self).get_context_data(**kwargs)
        context['collection'] = self.collection
        return context


@cart_required
def checkout(request, template_name='checkout.html'):
    if not request.user.is_authenticated():
        request.session['checkout'] = 'True'
        return HttpResponseRedirect(reverse('customer-register'))

    customer = request.user.customer
    with cart(request) as session_cart:
        order_total = session_cart.get_price()

    if not customer.country.shippingregion_set.all():
        return HttpResponseRedirect(reverse('store_unshippable'))

    if request.method == 'POST':
        # shipping_form = OrderForm(customer, request.POST)
        # payment_form = PaymentForm(request.POST)

        if shipping_form.is_valid():
            shipping_choice = shipping_form.cleaned_data['shipping_choice']
            order_total += Decimal(shipping_choice.cost)
            request.session['shipping_choice'] = shipping_choice.id

        if payment_form.is_valid():
            payment_option = payment_form.cleaned_data['payment_option']
            request.session['payment_option'] = payment_option.id

        if payment_form.is_valid() and shipping_form.is_valid():
            return HttpResponseRedirect(reverse(submit_order))
    else:
        # shipping_form = OrderForm(customer)
        # payment_form = PaymentForm()
        pass

    return render(
        request,
        template_name,
        {
            'customer': customer,
            # 'shipping_form': shipping_form,
            # 'payment_form': payment_form,
            'order_total': order_total,
        }
    )


@login_required
def unshippable(request, template_name='store/unshippable.html'):
    customer = request.user.customer

    if customer.country.shippingregion_set.all():
        url = request.META.get('HTTP_REFERER', None)
        if url is None:
            url = reverse('store')
        return HttpResponseRedirect(url)

    return render(
        template_name,
        {
            'customer': request.user.customer,
        }
    )


@login_required
def success(request, template_name='store/success.html'):
    return render(request, template_name)
