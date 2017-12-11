from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from . models import Launch, Entrie, Exit
from . forms import EntrieForm, ExitForm
from core.utils import Utils
from django.contrib import messages
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
	Table, TableStyle)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib import colors
from django.core.files.storage import FileSystemStorage

@login_required
def index(request):
	launches = Launch.getLaunches(request.user)
	(n_entries, n_exits, amount_entries,
		amount_exits, _, _) = Launch.statisticData(launches)
	
	context = {
	'launches': launches,
	'gain': (amount_entries - amount_exits),
	'entrieForm': EntrieForm,
	'exitForm': ExitForm}
	return render(request, 'cashjournal/index.html',
		context)

@login_required
def new_entrie(request):
	entrieForm = EntrieForm(request.POST)
	if entrieForm.is_valid():
		value = Utils.validate_value(entrieForm.cleaned_data['value'])
		if value is False:
			messages.add_message(request, messages.INFO, "Por favor! "
				" digite um valor numérico no campo valor")
		else:
			entrie = Entrie(
				description=entrieForm.cleaned_data['description'],
				value=value,
				user=request.user,
				l_type='en',
				en_type=entrieForm.cleaned_data['en_type'],
				)
			entrie.save()
			messages.add_message(request, messages.INFO, "Entrada registrada"
				" com sucesso")
	else:
		messages.add_message(request, messages.INFO, entrieForm.errors)
	return redirect('cashjournal:index')

@login_required
def new_exit(request):
	exitForm = ExitForm(request.POST)
	if exitForm.is_valid():
		value = Utils.validate_value(exitForm.cleaned_data['value'])
		if value is False:
			messages.add_message(request, messages.INFO, "Por favor! "
				" digite um valor numérico no campo valor")
		else:
			exit = Exit(
				description=exitForm.cleaned_data['description'],
				value=value,
				user=request.user,
				l_type='ex',
				ex_type=exitForm.cleaned_data['ex_type'],
				)
			exit.save()
			messages.add_message(request, messages.INFO, "Saída registrada"
				" com sucesso")
	else:
		messages.add_message(request, messages.INFO, exitForm.errors)
	return redirect('cashjournal:index')

def edit_launch(request, launch_id):
	launch = Launch.objects.get(id=launch_id)
	form = None
	context = {'launch_id': launch_id}
	data = {'description': launch.description, 'value': launch.value}
	template_name = None

	if launch.l_type == 'en':
		entrie = Entrie.getForLaunchId(launch.id)
		data.update({'en_type': entrie.en_type})
		form = EntrieForm(initial=data)
		context.update({'form': form})
		template_name = 'cashjournal/edit_entrie.html'
		
	else:
		exit = Exit.getForLaunchId(launch.id)
		data.update({'ex_type': exit.ex_type})
		form = ExitForm(initial=data)
		context.update({'form': form})
		template_name = 'cashjournal/edit_exit.html'
		
	return render(request, template_name , context)

def run_edit_entrie(request, launch_id):
	msg = ""
	value = Utils.validate_value(request.POST['value'])
	if value is False:
		messages.add_message(request, messages.INFO, "Por favor! "
			" digite um valor numérico no campo valor")
		return redirect('cashjournal:index')
	else:
		if Entrie.editType(launch_id, request.POST['en_type']):
			"""Entrie went updated or not went modified"""
			data = {'description': request.POST['description'],
			'value': value, 'launch_id': launch_id}
			if Launch.editLaunch(data):
				messages.add_message(request, messages.INFO,
					"Operação realizada com sucesso!")
				return redirect('cashjournal:index')	
			else:
				messages.add_message(request, messages.INFO,
					"Não foi possível executar a operação")
				return redirect('cashjournal:index')	

		

def run_edit_exit(request, launch_id):
	msg = ""
	value = Utils.validate_value(request.POST['value'])
	if value is False:
		messages.add_message(request, messages.INFO, "Por favor! "
			" digite um valor numérico no campo valor")
		return redirect('cashjournal:index')
	else:
		if Exit.editType(launch_id, request.POST['ex_type']):
			"""Entrie went updated or not went modified"""
			data = {'description': request.POST['description'],
			'value': value, 'launch_id': launch_id}
			if Launch.editLaunch(data):
				messages.add_message(request, messages.INFO,
					"Operação realizada com sucesso!")
				return redirect('cashjournal:index')	
			else:
				messages.add_message(request, messages.INFO,
					"Não foi possível executar a operação")
				return redirect('cashjournal:index')

def delete_entrie(request, launch_id):
	if Entrie.deleteEntrie(launch_id):
		if Launch.deleteLaunch(launch_id):
			messages.add_message(request, messages.INFO,
				"Entrada deletada com sucesso")
		else:
			messages.add_message(request, messages.INFO,
				"Não foi possível deletar a entrada")
	else:
		messages.add_message(request, messages.INFO,
			"Não foi possível deletar a entrada")

	return redirect('cashjournal:index')

def delete_exit(request, launch_id):
	if Exit.deleteExit(launch_id):
		if Launch.deleteLaunch(launch_id):
			messages.add_message(request, messages.INFO,
				"Saída deletada com sucesso")
		else:
			messages.add_message(request, messages.INFO,
				"Não foi possível deletar a saída")
	else:
		messages.add_message(request, messages.INFO,
			"Não foi possível deletar a saída")

	return redirect('cashjournal:index')

def search_launches(request, **kwargs):
	# data for search in database
	init_date = kwargs['year1'] + '-' + kwargs['month1'] + '-' + kwargs['day1']
	end_date = kwargs['year2'] + '-' + kwargs['month2'] + '-' + kwargs['day2']

	launches = Launch.getLaunchesPeriod(request,
		init_date, end_date)
	# data for showing
	init_date = kwargs['day1'] + '/' + kwargs['month1'] + '/' + kwargs['year1']
	end_date = kwargs['day2'] + '/' + kwargs['month2'] + '/' + kwargs['year2']
	
	(n_entries, n_exits, amount_entries, amount_exits,
	 list_entries, list_exits) = Launch.statisticData(launches)
	
	context = {
		'launches': launches,
		'init_date': init_date, 'end_date': end_date,
		'amount_entries': amount_entries, 'amount_exits': amount_exits,	
		'gain': (amount_entries - amount_exits)
	}



	if list_entries:
		context.update({'list_entries': list_entries})
		
	if list_exits:
		context.update({'list_exits': list_exits})

	return render(request, 'cashjournal/search_launches.html', context)

def generate_report(request, **kwargs):
	# data for search in database
	init_date = kwargs['year1'] + '-' + kwargs['month1'] + '-' + kwargs['day1']
	end_date = kwargs['year2'] + '-' + kwargs['month2'] + '-' + kwargs['day2']
	
	launches = Launch.getLaunchesPeriod(request,
		init_date, end_date)

	# data for showing
	init_date = kwargs['day1'] + '/' + kwargs['month1'] + '/' + kwargs['year1']
	end_date = kwargs['day2'] + '/' + kwargs['month2'] + '/' + kwargs['year2']

	(n_entries, n_exits, amount_entries, amount_exits,
	 list_entries, list_exits) = Launch.statisticData(launches)

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

	# Entries
	txt_intro_entries = "Entradas"
	p = Paragraph(txt_intro_entries, styles['Heading2'])
	Catalog.append(p)
	Catalog.append(Spacer(1, 0.2 * inch))

	detail_entries = """
	Ao longo desse período foram registradas {} entradas somando um 
	montante de R$ {}
	""".format(n_entries, amount_entries)
	p = Paragraph(detail_entries, styles['Normal'])
	Catalog.append(p)
	Catalog.append(Spacer(1, 0.2 * inch))

	headings = ('Data','Descrição', 'Valor R$', 'Tipo')
	allentries = [(Utils.reverse_date(entrie.date), entrie.description, entrie.value, Entrie.enType(entrie.en_type)) for entrie in list_entries]
	
	t_entries = Table([headings] + allentries)
	t_entries.setStyle(TableStyle(
			[
				('GRID', (0,0), (-1,-1), 1, colors.blue),
				('LINEBELOW', (0,0), (-1, 0), 1, colors.black),
				('BACKGROUND', (0, 0), (-1, 0), colors.yellow),
				('ALIGN', (1,1), (-1,-1), 'CENTER')
			]
		)
	)

	Catalog.append(t_entries)
	# End Entries

	# Exits
	txt_intro_exts = "Saídas"
	p = Paragraph(txt_intro_exts, styles['Heading2'])
	Catalog.append(p)
	Catalog.append(Spacer(1, 0.2 * inch))

	detail_exts = """
	Ao longo desse período foram registradas {} saídas somando um 
	montante de R$ {}
	""".format(n_exits, amount_exits)
	p = Paragraph(detail_exts, styles['Normal'])
	Catalog.append(p)
	Catalog.append(Spacer(1, 0.2 * inch))

	headings = ('Data','Descrição', 'Valor R$', 'Tipo')
	allexts = [(Utils.reverse_date(exit.date), exit.description, exit.value, Exit.exType(exit.ex_type)) for exit in list_exits]
	
	t_exts = Table([headings] + allexts)
	t_exts.setStyle(TableStyle(
			[
				('GRID', (0,0), (-1,-1), 1, colors.blue),
				('LINEBELOW', (0,0), (-1, 0), 1, colors.black),
				('BACKGROUND', (0, 0), (-1, 0), colors.yellow),
				('ALIGN', (1,1), (-1,-1), 'CENTER')
			]
		)
	)

	Catalog.append(t_exts)
	# End Exits

	Catalog.append(Spacer(1, 0.3 * inch))

	amount = amount_entries - amount_exits
	result = None
	if amount >= 0:
		result = "Lucro: R$ {}".format(amount)
	else:
		prejuizo = amount + (2 * result)
		result = "Prejuízo: R$ {}".format(prejuizo)

	p = Paragraph(result, styles['Heading2'])
	Catalog.append(p)
	
	doc.build(Catalog)
	fs = FileSystemStorage("/tmp")
	with fs.open("report.pdf") as pdf:
		response = HttpResponse(pdf, content_type='application/pdf')
		response['Content-Disposition'] = 'attachment; filename="relatorio.pdf"'
	
	return response