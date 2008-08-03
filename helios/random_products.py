#!/usr/bin/env python
import sys
from string import Template
from random import randint, random
from datetime import datetime


if len(sys.argv) <= 1:
	print 'Usage: python random_products.py <num_of_products>\n'
	sys.exit(1)

product_insert_multilingual = """
insert into store_product (slug, category_id, date_added, is_active, stock, weight, price)
	values ('$slug', category_id, '$date_added', 1, 0, 0, $price);

insert into store_producttranslation (name, desc, language_id, master_id) values ($name, '', 1, 1);
insert into store_producttranslation (name, desc, language_id, master_id) values ($name, '', 2, 1);
"""

product_insert = """
INSERT INTO store_product (name, slug, desc, category_id, date_added, is_active, stock, weight, price)
	VALUES ('$name','$slug', '', $category_id, '$date_added', 1, 0, 0, $price);
"""

product_template = Template(product_insert)

today = datetime.now().date().isoformat()

for i in range(int(sys.argv[1])):
	print product_template.substitute(name='My Product'+str(i), slug='my-product'+str(i),
		category_id=randint(1, 13), date_added=today, price=i)
