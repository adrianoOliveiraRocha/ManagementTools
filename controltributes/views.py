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
	
	payments_list = Payment.getPayments(request.user.id)
	for payment in payments_list:
		print(payment)
	
	tribute_choices = Tribute.getTributeChoices(request.user.id)
	context = {
		'tributeForm': tributeForm,
		'tributes': tributes,
		'tribute_choices': tribute_choices
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
