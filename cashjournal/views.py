from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from . models import Launch, Entrie, Exit
from . forms import EntrieForm, ExitForm
from core.utils import Utils
from django.contrib import messages

@login_required
def index(request):
	launches = Launch.getLaunches(request.user)
	(n_entries, n_exits, amount_entries, amount_exits) = Launch.statisticData(launches)
	
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
	return HttpResponse('Calling delete_entrie')

def delete_exit(request, launch_id):
	return HttpResponse('Calling delete_exit')
