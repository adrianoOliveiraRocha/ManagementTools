from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^index$', views.index, name='index'),
	url(r'^new_entrie$', views.new_entrie, name='new_entrie'),
	url(r'^new_exit$', views.new_exit, name='new_exit'),
	url(r'^edit_launch/(?P<launch_id>\d+)$',
		views.edit_launch, name='edit_launch'),
	url(r'^run_edit_entrie/(?P<launch_id>\d+)$',
		views.run_edit_entrie, name='run_edit_entrie'),
	url(r'^run_edit_exit/(?P<launch_id>\d+)$',
		views.run_edit_exit, name='run_edit_exit'),
	url(r'^delete_entrie/(?P<launch_id>\d+)$',
		views.delete_entrie, name='delete_entrie'),
	url(r'^delete_exit/(?P<launch_id>\d+)$',
		views.delete_exit, name='delete_exit'),
]