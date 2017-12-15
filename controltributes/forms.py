from django import forms
from . models import Tribute, Payment


class TributeForm(forms.Form):
	description = forms.CharField(label='Descrição', required=False)
	period = forms.CharField(label='Período de Pagamento', required=False)
	

	
	