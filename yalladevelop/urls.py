''' This will be the URL Dispatcher, i.e., the file that will be in charge of
linking the pages to the controller '''

from django.conf.urls import patterns, url
from django.contrib.auth import authenticate, login
from yalladevelop import views

urlpatterns = patterns('',
	# Examples: 
	url(r'^$', views.index, name='index'), #links to Home page
	# url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'Photographia/login.html'}, name="login"),
	# url(r'^logout/$', views.logout_user, name="logout"),
)