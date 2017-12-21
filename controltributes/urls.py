from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^index$', views.index, name='index'),
	url(r'^new_tribute$', views.new_tribute, name='new_tribute'),
	url(r'^new_payment$', views.new_payment, name='new_payment'),
	url(r'^edit_tribute/(?P<tribute_id>\d+)$',
		views.edit_tribute, name='edit_tribute'),
	url(r'^run_edit_tribute/(?P<tribute_id>\d+)$',
		views.run_edit_tribute, name='run_edit_tribute'),
	url(r'^delete_tribute/(?P<tribute_id>\d+)$',
		views.delete_tribute, name='delete_tribute'),
	url(r'^payments_relateds/(?P<tribute_id>\d+)$',
		views.payments_relateds, name='payments_relateds'),
]