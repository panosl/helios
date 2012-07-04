from django.db import models
from django.utils.translation import ugettext_lazy as _
from helios.location.models import Country
from helios.conf import settings
if settings.IS_MULTILINGUAL:
    import multilingual


class PaymentOption(models.Model):
    if settings.IS_MULTILINGUAL:
        class Translation(multilingual.Translation):
            name = models.CharField(_('name'), max_length=80)
            desc = models.TextField(_('description'), blank=True)
    else:
        name = models.CharField(_('name'), max_length=80)
        desc = models.TextField(_('description'), blank=True)

    slug = models.SlugField(unique=True, max_length=80)
    supported_countries = models.ManyToManyField(Country, blank=True, null=True)

    class Meta:
        verbose_name = _('payment option')
        verbose_name_plural = _('payment options')
        pass

    def __unicode__(self):
        return self.name
