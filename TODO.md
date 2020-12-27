Helios
======

Long Term
---------

 * Standing of the customer:
    How trustworthy is the customer? It should depend on a ratio of orders/payed_orders.
    If he's standing is low, feature orders should be verified by phone.
 * SMS updates of new (approved) checkouts.
 * Newsletter.
 * Wishlist.
 * RSS feed of new products added.
 * Registered users, should be able to:
    - comment on a product,
    - rate a product,
    - mark a product as insultive.
 * Move customer creation to a Wizard (Django 1.0)


Documentation Goals
===================

 * Development documentation
    What each app does.
 * HOWTO documentation
    Extend a specific application of helios or helios itself. Add a new app, how to
    integrate it to your own site.
 * User documentation
    Actually this is intented as admin/manager documents. Explaining how a user can
    work with helios, adding/removing stuff through the admin section.
    This might be extended in the feature. Keep in mind that we should not be lead
    astray from the admin app. Each addition should be done there, and not through
    individual generic or not forms.
