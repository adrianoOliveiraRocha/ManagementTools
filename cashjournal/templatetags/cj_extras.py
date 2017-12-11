from django import template
from cashjournal.models import Entrie

register = template.Library()

@register.simple_tag
def type_test(launch):
	if launch.l_type == 'en':
		return 'Entrada'
	else:
		return 'Saída'

@register.simple_tag
def en_type(code):
	if code == 'mo':
		return 'Dinheiro'
	elif code == 'ch':
		return 'Cheque'
	elif code == 'de':
		return 'Débito'
	elif code == 'cr':
		return 'Crédito'
	elif code == 'tr':
		return 'Transferência'
	elif code == 'dp':
		return 'Depósito'
	elif code == 'ot':
		return 'Outro'

@register.simple_tag
def ex_type(code):
	if code == 'pa':
		return 'Pagamento'
	elif code == 'cw':
		return 'Retirada'
