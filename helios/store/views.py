# -*- coding: utf-8 -*-
from __future__ import with_statement
from datetime import datetime
from decimal import Decimal
from django.core.mail import send_mail, mail_managers
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.views.generic.list_detail import object_list
from django.views.generic import DetailView
from helios.conf import settings
from helios.orders.models import OrderStatus, Order, OrderLine
from helios.orders.forms import OrderForm
from helios.shipping.models import ShippingMethodRegions
from helios.store.models import Product, Category, Collection
from helios.store.cart import cart
from helios.payment.models import PaymentOption
from helios.payment.forms import PaymentForm
from helios.store.decorators import cart_required
if settings.USE_PAYPAL:
    from helios.paypal.views import *


class ProductDetail(DetailView):
    context_object_name = 'product'
    queryset = Product.objects.all()
    model = Product

    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data(**kwargs)
        context['category'] = self.get_object().category
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
        items_in_stock = session_cart[product_id].get_product().stock

        if quantity < 0:
            return HttpResponseRedirect(success_url)
        elif quantity == 0 or items_in_stock == 0:
            del session_cart[product_id]
        else:
            if quantity >= items_in_stock:
                session_cart[product_id]['quantity'] = items_in_stock
            else:
                session_cart[product_id]['quantity'] = quantity

    return HttpResponseRedirect(success_url)


def product_add(request, slug=''):
    try:
        product = Product.objects.get(slug=slug)
    except Product.DoesNotExist:
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
        product = Product.objects.get(slug=slug)
    except Product.DoesNotExist:
        return HttpResponse('That product does not exist.')

    with cart(request) as session_cart:
        try:
            session_cart.remove_product(product.id)
        except KeyError:
            return HttpResponse('Does not have one of those!')

    return HttpResponseRedirect(reverse('store_cart'))


def category_list(request, category, **kwargs):
    category = get_object_or_404(Category, slug=category)
    #TODO include the category along with the children
    if category.is_root_node():
        product_list = Product.objects.filter(category__slug__in=(c.slug for c in category.get_children()))
    else:
        product_list = Product.objects.filter(category__slug__exact=category.slug)
    kwargs['extra_context']['category'] = category

    return object_list(request, queryset=product_list, **kwargs)

def collection_list(request, collection, **kwargs):
    collection = get_object_or_404(Collection, slug=collection)
    #product_list = Product.objects.filter(category__slug__exact=category.slug)
    product_list = collection.products.all()
    kwargs['extra_context']['collection'] = collection

    return object_list(request, queryset=product_list, **kwargs)


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
        #shipping_form = OrderForm(customer, request.POST,
            #initial={'shipping_choice': request.POST['shipping_choice']})
        shipping_form = OrderForm(customer, request.POST)
        payment_form = PaymentForm(request.POST)

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
        shipping_form = OrderForm(customer)
        payment_form = PaymentForm()

    return render_to_response(template_name,
        {
            'customer': customer,
            'shipping_form': shipping_form,
            'payment_form': payment_form,
            'order_total': order_total,
        },
        context_instance=RequestContext(request))


@login_required
def unshippable(request, template_name='store/unshippable.html'):
    customer = request.user.customer

    if customer.country.shippingregion_set.all():
        url = request.META.get('HTTP_REFERER', None)
        if url is None:
            url = reverse('store')
        return HttpResponseRedirect(url)
    return render_to_response(template_name, {
            'customer': request.user.customer,
    },
    context_instance=RequestContext(request))


@cart_required
@login_required
def submit_order(request, template_name='checkout.html'):
    try:
        shipping_choice = ShippingMethodRegions.objects.get(pk=request.session['shipping_choice'])
    except KeyError:
        request.user.message_set.create(message=_(u'%s you haven\'t chosen a shipping method.') % (request.user.username,))
        return HttpResponseRedirect(reverse('store_checkout'))

    try:
        payment_option = PaymentOption.objects.get(pk=request.session['payment_option'])
    except KeyError:
        request.user.message_set.create(message=_(u'%s you haven\'t chosen a payment option.') % (request.user.username,))
        return HttpResponseRedirect(reverse('store_checkout'))

    customer = request.user.customer

    if payment_option.slug == 'paypal':
        return HttpResponseRedirect(reverse(paypal_purchase))

    order_dict = {
        'date_time_created': datetime.today(),
        'customer': customer,
        'status': OrderStatus.objects.get(slug__exact='pending'),
        'shipping_city': customer.city,
        'shipping_country': customer.country,
        'shipping_choice': shipping_choice,
        'payment_option': payment_option
    }

    if request.session['currency']:
        order_dict['currency_code'] = request.session['currency'].code
        order_dict['currency_factor'] = request.session['currency'].factor
    order = Order.objects.create(**order_dict)

    with cart(request) as session_cart:
        for cart_line in session_cart.values():
            order_line = OrderLine.objects.create(
                order=order,
                product=cart_line.get_product(),
                unit_price=cart_line.get_product().price,
                price=cart_line.get_price(),
                quantity=cart_line.get_quantity()
            )
        session_cart.clear()

    #TODO maybe turn this into a signal
    subject = render_to_string('store/order_subject.txt', {'order': order})

    send_mail(''.join(subject.splitlines()), render_to_string('store/order.txt', {'order': order, 'customer': customer, 'country': customer.country }), 'noreply@holabyolga.gr', [customer.email])
    mail_managers(''.join(subject.splitlines()), render_to_string('store/order.txt', {'order': order, 'customer': customer, 'country': customer.country }), fail_silently=False)

    return HttpResponseRedirect(reverse(success))


@login_required
def success(request, template_name='order_success.html'):
    return render_to_response(template_name, context_instance=RequestContext(request))
