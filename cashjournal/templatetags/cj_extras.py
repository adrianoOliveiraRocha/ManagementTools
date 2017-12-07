from django import template
from cashjournal.models import Entrie

register = template.Library()

@register.simple_tag
def type_test(launch):
	if launch.l_type == 'en':
		return 'Entrada'
	else:
		return 'Saída'