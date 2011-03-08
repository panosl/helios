from django import template
from template_utils.nodes import ContextUpdatingNode, GenericContentNode


class FeaturedContentNode(GenericContentNode):
	def _get_query_set(self):
		return self.query_set.filter(is_featured__exact=True)


def do_featured_object(parser, token):
	"""
	Retrieves the latest object from a given model, in that model's
	default ordering, and stores it in a context variable.

	Syntax::

	{% get_latest_object [app_name].[model_name] as [varname] %}

	Example::

	{% get_latest_object comments.freecomment as latest_comment %}
	"""
	bits = token.contents.split()
	if len(bits) != 4:
		raise template.TemplateSyntaxError("'%s' tag takes three arguments" % bits[0])
	if bits[2] != 'as':
		raise template.TemplateSyntaxError("second argument to '%s' tag must be 'as'" % bits[0])
	return FeaturedContentNode(bits[1], 1, bits[3])

register = template.Library()
register.tag('get_featured_object', do_featured_object)
