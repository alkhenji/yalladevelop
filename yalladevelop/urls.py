''' This will be the URL Dispatcher, i.e., the file that will be in charge of
linking the pages to the controller '''

from django.conf.urls import patterns, url
from django.contrib.auth import authenticate, login
from yalladevelop import views

urlpatterns = patterns('',
	# Examples: 
	url(r'^$', views.index, name='index'), #links to Home page
	url(r'^signup/$', views.signup_user, name="signup"),
	url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'yalladevelop/login.html'}, name="login"),
	url(r'^logout/$', views.logout_user, name="logout"),
	url(r'^project/(?P<project_id>\d+)/$', views.showProject, name='showProject'),
	url(r'^profile/(?P<profile_id>\d+)/$', views.showProfile, name='showProfile'),
	url(r'^profile/(?P<profile_id>\d+)/$', views.showProfile, name='showProfile'),

	# Static Pages Dispatcher
	url(r'^about/$', views.about, name="about"),
	url(r'^contact/$', views.contact, name="contact"),
	url(r'^explore/$', views.explore, name="explore"),
	url(r'^faq/$', views.faq, name="faq"),
	url(r'^help/$', views.help, name="help"),
	url(r'^privacy/$', views.privacy, name="privacy"),
	url(r'^sitemap/$', views.sitemap, name="sitemap"),
	url(r'^terms/$', views.terms, name="terms"),
	
	url(r'^111/$', views.test, name="test"),
)