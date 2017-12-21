from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from controltributes.models import Tribute, Payment
from . forms import TributeForm
from core.utils import Utils
from django.contrib import messages
from django.contrib.sessions.backends.db import SessionStore

@login_required
def index(request):
	
	tributeForm = TributeForm()
	tributes = Tribute.getTributes(request.user.id)
	
	payments_list = Payment.getPaymentsForTributes(request.user.id)
		
	tribute_choices = Tribute.getTributeChoices(request.user.id)
	context = {
		'tributeForm': tributeForm,
		'tributes': tributes,
		'tribute_choices': tribute_choices,
		'payments_list': payments_list
	}
	
	return render(request, 'controltributes/index.html',
		context)

@login_required
def new_tribute(request):
	tributeForm = TributeForm(request.POST)
	if tributeForm.is_valid():
		tribute = Tribute(
			description=tributeForm.cleaned_data['description'],
			period=tributeForm.cleaned_data['period'],
			user_id=request.user.id
			)
		tribute.save()
		messages.add_message(request, messages.INFO, "Tributo registrado"
			" com sucesso")
	else:
		messages.add_message(request, messages.INFO, entrieForm.errors)
	
	return redirect('controltributes:index')

@login_required
def new_payment(request):
	id_tribute = request.POST['tribute']
	value = Utils.validate_value(request.POST['payment_value'])
	if not value:
		messages.add_message(request, messages.INFO, "Por favor,"
			" preencha o campo valor corretamente")
	else:
		payment = Payment(
			value=value,
			tribute=Tribute.objects.get(id=id_tribute))
		try:
			payment.save()
			messages.add_message(request, messages.INFO, "Pagamento"
			" registrado com sucesso!")
		except Exception as e:
			raise e
	return redirect('controltributes:index')

@login_required
def edit_tribute(request, tribute_id):
	tribute = Tribute.objects.get(id=tribute_id)
	data = {'description': tribute.description, 'period': tribute.period}
	form = TributeForm(initial=data)
	context = {'tribute_id': tribute_id, 'form': form}
	template_name = 'controltributes/edit_tribute.html'
		
	return render(request, 'controltributes/edit_tribute.html', context)

def run_edit_tribute(request, tribute_id):
	data = {'description': request.POST['description'],
	'period': request.POST['period']}

	result = Tribute.editTribute(data, tribute_id)

	if not result:
		messages.add_message(request, messages.INFO, "Erro"
			" ao tentar editar o tributo!")
	else:
		messages.add_message(request, messages.INFO, result)

	return redirect('controltributes:index')

def delete_tribute(request, tribute_id):
	tribute = Tribute.objects.get(id=tribute_id)
	tribute.delete()
	messages.add_message(request, messages.INFO, "Tributo"
			" deletedo com sucesso!")
	return redirect('controltributes:index')

def payments_relateds(request, tribute_id):
	payments, sum_payments, tribute_description = Payment.getPaymentsRelateds(tribute_id)
	
	context = {
		'payments': payments,
		'tribute_description': tribute_description,
		'sum_payments': sum_payments
	}
	return render(request, 'controltributes/payments_relateds.html', context)

