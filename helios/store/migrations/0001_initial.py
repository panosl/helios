# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tax'
        db.create_table('store_tax', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('desc', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=80)),
            ('rate', self.gf('django.db.models.fields.DecimalField')(default=19.0, max_digits=4, decimal_places=2)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('store', ['Tax'])

        # Adding model 'Category'
        db.create_table('store_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('desc', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='child_set', null=True, to=orm['store.Category'])),
        ))
        db.send_create_signal('store', ['Category'])

        # Adding model 'Product'
        db.create_table('store_product', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('desc', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=80)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['store.Category'], null=True, blank=True)),
            ('date_added', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_featured', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('stock', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('weight', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('base_price', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
        ))
        db.send_create_signal('store', ['Product'])

        # Adding M2M table for field taxes on 'Product'
        db.create_table('store_product_taxes', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('product', models.ForeignKey(orm['store.product'], null=False)),
            ('tax', models.ForeignKey(orm['store.tax'], null=False))
        ))
        db.create_unique('store_product_taxes', ['product_id', 'tax_id'])

        # Adding model 'ProductImage'
        db.create_table('store_productimage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['store.Product'], null=True, blank=True)),
            ('picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('store', ['ProductImage'])

        # Adding model 'PaymentOption'
        db.create_table('store_paymentoption', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('desc', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=80)),
        ))
        db.send_create_signal('store', ['PaymentOption'])

        # Adding M2M table for field supported_countries on 'PaymentOption'
        db.create_table('store_paymentoption_supported_countries', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('paymentoption', models.ForeignKey(orm['store.paymentoption'], null=False)),
            ('country', models.ForeignKey(orm['location.country'], null=False))
        ))
        db.create_unique('store_paymentoption_supported_countries', ['paymentoption_id', 'country_id'])


    def backwards(self, orm):
        # Deleting model 'Tax'
        db.delete_table('store_tax')

        # Deleting model 'Category'
        db.delete_table('store_category')

        # Deleting model 'Product'
        db.delete_table('store_product')

        # Removing M2M table for field taxes on 'Product'
        db.delete_table('store_product_taxes')

        # Deleting model 'ProductImage'
        db.delete_table('store_productimage')

        # Deleting model 'PaymentOption'
        db.delete_table('store_paymentoption')

        # Removing M2M table for field supported_countries on 'PaymentOption'
        db.delete_table('store_paymentoption_supported_countries')


    models = {
        'location.country': {
            'Meta': {'object_name': 'Country'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'})
        },
        'store.category': {
            'Meta': {'ordering': "['slug']", 'object_name': 'Category'},
            'desc': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'child_set'", 'null': 'True', 'to': "orm['store.Category']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        'store.paymentoption': {
            'Meta': {'object_name': 'PaymentOption'},
            'desc': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '80'}),
            'supported_countries': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['location.Country']", 'null': 'True', 'blank': 'True'})
        },
        'store.product': {
            'Meta': {'ordering': "['name']", 'object_name': 'Product'},
            'base_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['store.Category']", 'null': 'True', 'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'desc': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '80'}),
            'stock': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'taxes': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['store.Tax']", 'null': 'True', 'blank': 'True'}),
            'weight': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'store.productimage': {
            'Meta': {'object_name': 'ProductImage'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['store.Product']", 'null': 'True', 'blank': 'True'})
        },
        'store.tax': {
            'Meta': {'object_name': 'Tax'},
            'desc': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'rate': ('django.db.models.fields.DecimalField', [], {'default': '19.0', 'max_digits': '4', 'decimal_places': '2'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '80'})
        }
    }

    complete_apps = ['store']