# -*- coding: utf-8 -*-
from datetime import datetime

from helios.shipping.models import ShippingMethodRegions
from helios.store.decorators import cart_required
from helios.payment.models import PaymentOption
from helios.orders.models import Order, OrderLine, OrderStatus


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


