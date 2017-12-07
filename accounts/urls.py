from django.conf.urls import url, include
from . import views

urlpatterns = [
	url(r'^registro/$', views.RegisterView.as_view(), name='register'),
]