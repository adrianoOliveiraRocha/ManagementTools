# coding=utf-8
from .models import Launch
from django import forms

class EntrieForm(forms.Form):
	TYPE_ENTRIE = (
		('mo', 'Dinheiro'),
		('ch', 'Cheque'),
		('de', 'Cartão de Débito'),
		('cr', 'Cartão de Crédito'),
		('tr', 'Transferência'),
		('dp', 'Depósito'),
		('ot', 'Outro')
	)

	description = forms.CharField(label='Descrição', required=False)
	value = forms.CharField(label='Valor R$', required=True,
		localize=True)
	en_type = forms.CharField(label='Tipo', max_length=2, required=True,
		widget=forms.Select(choices=TYPE_ENTRIE),)


class ExitForm(forms.Form):
	TYPE_EXIT = (
		('pa', 'Pagamento'),
		('cw', 'Retirada'),
	)
	
	description = forms.CharField(label='Descrição')
	value = forms.CharField(label='Valor R$', required=True,
		localize=True)
	ex_type = forms.CharField(label='Tipo', max_length=2, required=True,
		widget=forms.Select(choices=TYPE_EXIT),)

