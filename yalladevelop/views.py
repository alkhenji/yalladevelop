''' This will be the Controller of the Application. Examples below. '''

from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect

# User forms
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Permission

# Authentication and Users
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.core.context_processors import csrf
from django.template import RequestContext

def index(request):
	user = request.user
	logged_in = request.user.is_authenticated()
	not_logged_in = not logged_in
	return render(request, 'yalladevelop/index.html', {'user':user,'logged_in':logged_in,'not_logged_in':not_logged_in})
	
def signup(request):
	return render(request, 'yalladevelop/signup.html', {})

@csrf_exempt
def signup_user(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			new_user = form.save()
			new_user = authenticate(username=request.POST['username'],password=request.POST['password1'])
			login(request, new_user)
			url = reverse('index')
			return HttpResponseRedirect(url)
	else:
		form = UserCreationForm()
	return render(request, "yalladevelop/signup.html", {'form': form})
	
def login_user(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username,password=password)
	if user:
		return render(request, 'yalladevelop/index.html')
	else:
		return HttpResponseRedirect('/')
		
def logout_user(request):
	logout(request)
	return HttpResponseRedirect('/')