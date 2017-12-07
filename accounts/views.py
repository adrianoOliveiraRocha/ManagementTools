from django.shortcuts import render
from django.views.generic import (CreateView, TemplateView, UpdateView, 
FormView)
from .models import User
from .forms import UserAdminCreationForm
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm


class RegisterView(CreateView):
	model = User
	template_name = 'accounts/register.html'
	form_class = UserAdminCreationForm
	success_url = reverse_lazy('index')
	
		

