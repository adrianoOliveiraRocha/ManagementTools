from django.conf.urls import url, include
from django.contrib import admin
from core import views as core
from django.contrib.auth.views import login, logout

urlpatterns = [
    url(r'^admin/', admin.site.urls),
	url(r'^entrar/$', login, {'template_name': 'login.html'}
		,name='login'),
	url(r'^sair/$', logout, {'next_page': 'index'}, name='logout'),
	url(r'^$', core.IndexView.as_view(), name='index'),
	url(r'^conta/', include('accounts.urls', namespace='accounts')),
	url(r'^cashjournal/', include('cashjournal.urls',
		namespace='cashjournal')),
	url(r'^controltributes/', include('controltributes.urls',
		namespace='controltributes')),
]
