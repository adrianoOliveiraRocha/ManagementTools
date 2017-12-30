from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from controltributes.models import Tribute, Payment
from . forms import TributeForm
from core.utils import Utils
from django.contrib import messages
from django.contrib.sessions.backends.db import SessionStore
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
	Table, TableStyle)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib import colors
from django.core.files.storage import FileSystemStorage
from cashjournal.models import Exit

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
		tribute = Tribute.objects.get(id=id_tribute)
		payment = Payment(
			value=value,
			tribute=tribute)
		try:
			payment.save()
			# register cashjournal exit
			data = {
				'description': tribute.description,
				'value': value,
				'l_type': 'ex',
				'user': request.user,
				'ex_type': 'cw'  
			}
			msg = None
			if Exit.registerExit(data):
				msg = 'O pagamento foi realizado com sucesso!'
			else:
				msg = 'O pagamento foi realizado mas a saída não registrada!'				
			messages.add_message(request, messages.INFO, msg)

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

def search_for_period(request, **kwargs):
	# data for search in database
	init_date = kwargs['year1'] + '-' + kwargs['month1'] + '-' + kwargs['day1']
	end_date = kwargs['year2'] + '-' + kwargs['month2'] + '-' + kwargs['day2']

	list_payments_for_tributes, amount, _ = Tribute.getTributesForPeriod(request.user.id, init_date, end_date)

	init_date = kwargs['day1'] + '/' + kwargs['month1'] + '/' + kwargs['year1']
	end_date = kwargs['day2'] + '/' + kwargs['month2'] + '/' + kwargs['year2']

	context = {
		'list_payments_for_tributes': list_payments_for_tributes,
		'init_date': init_date, 'end_date': end_date,
		'amount': amount
		}

	return render(request, 'controltributes/show_payments_for_tributes.html', context)
	
def report_generate(request, **kwargs):
	# data for search in database
	init_date = kwargs['year1'] + '-' + kwargs['month1'] + '-' + kwargs['day1']
	end_date = kwargs['year2'] + '-' + kwargs['month2'] + '-' + kwargs['day2']

	list_payments_for_tributes, amount, n_payments  = Tribute.getTributesForPeriod(request.user,
		init_date, end_date)

	# data for showing
	init_date = kwargs['day1'] + '/' + kwargs['month1'] + '/' + kwargs['year1']
	end_date = kwargs['day2'] + '/' + kwargs['month2'] + '/' + kwargs['year2']

	doc = SimpleDocTemplate("/tmp/report.pdf")
	Catalog = []
	styles = getSampleStyleSheet()
	style = styles["Normal"]

	header = Paragraph("Relatório", styles['Heading1'])
	Catalog.append(header)

	txt_intro = """
	Período Base {} à {}
	""".format(init_date, end_date)
	p = Paragraph(txt_intro, styles['Heading3'])
	Catalog.append(p)
	Catalog.append(Spacer(1, 1))

	# Payments
	txt_intro_payments = "Pagamentos"
	p = Paragraph(txt_intro_payments, styles['Heading2'])
	Catalog.append(p)
	Catalog.append(Spacer(1, 0.2 * inch))

	detail_payments = """ Durante esse período, foram registrados {} pagamentos
	com um montante de R$ {}
	""".format(n_payments, amount)
	p = Paragraph(detail_payments, styles['Normal'])
	Catalog.append(p)
	Catalog.append(Spacer(1, 0.2 * inch))

	headings = ('Descrição','Período de Pagamento', 'Data de Pagamento', 'Valor R$')
	allpayments = [(payment[0], payment[1], Utils.reverse_date(payment[2]), payment[3]) for payment in list_payments_for_tributes]

	t_payments = Table([headings] + allpayments)
	t_payments.setStyle(TableStyle(
			[
				('GRID', (0,0), (-1,-1), 1, colors.blue),
				('LINEBELOW', (0,0), (-1, 0), 1, colors.black),
				('BACKGROUND', (0, 0), (-1, 0), colors.yellow),
				('ALIGN', (1,1), (-1,-1), 'CENTER')
			]
		)
	)

	Catalog.append(t_payments)

	doc.build(Catalog)
	fs = FileSystemStorage("/tmp")
	with fs.open("report.pdf") as pdf:
		response = HttpResponse(pdf, content_type='application/pdf')
		response['Content-Disposition'] = 'attachment; filename="relatorio.pdf"'
	
	return response
