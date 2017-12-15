from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^index$', views.index, name='index'),
	url(r'^new_tribute$', views.new_tribute, name='new_tribute'),
	url(r'^new_payment$', views.new_payment, name='new_payment'),
]