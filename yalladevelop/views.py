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

#Models
from yalladevelop.models import Project, Skill, UserProfile
from yalladevelop.forms import UserCreateForm

def index(request):
	user = request.user
	logged_in = request.user.is_authenticated()
	not_logged_in = not logged_in
	return render(request, 'yalladevelop/index.html', {'user':user,'logged_in':logged_in,'not_logged_in':not_logged_in,'page_name':"Home"})
	
def showProject(request,project_id):
	project = Project.objects.filter(id=project_id)
	if project:
		project = project[0] 
		owner = User.objects.filter(id=project.user_id)[0]
		return render(request,'yalladevelop/project.html', {'project':project, 'owner': owner})
	else:
		return render(request, 'yalladevelop/404.html')

def showProfile(request,profile_id):
	userProfile = UserProfile.objects.filter(id=profile_id)
	if userProfile:
		userProfile = userProfile[0]
		userAccount = User.objects.get(id=profile_id)
		skills = userProfile.skill.all()
		return render(request,'yalladevelop/profile.html', {'userProfile': userProfile, 'skills':skills,'userAccount':userAccount})
	else:
		return render(request, 'yalladevelop/404.html')
	
# -------------------- Authentication ----------------------
def signup(request):
	return render(request, 'yalladevelop/signup.html', {})

@csrf_exempt
def signup_user(request):
	if request.method == 'POST':
		# form = UserCreationForm(request.POST)
		form = UserCreateForm(request.POST)
		if form.is_valid():
			new_user = form.save()
			new_user = authenticate(username=request.POST['username'],password=request.POST['password1'])
			login(request, new_user)
			url = reverse('index')
			return HttpResponseRedirect(url)
	else:
		# form = UserCreationForm()
		form = UserCreateForm()
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
	
	
	
# -------------------- Static Pages -------------------------

def about(request):
	return render(request, 'yalladevelop/about.html', {})
	
def contact(request):
	return render(request, 'yalladevelop/contact.html', {})
	
def explore(request):
	return render(request, 'yalladevelop/explore.html', {})

def faq(request):
	return render(request, 'yalladevelop/faq.html', {})
	
def help(request):
	return render(request, 'yalladevelop/help.html', {})
	
def privacy(request):
	return render(request, 'yalladevelop/privacy.html', {})
	
def sitemap(request):
	return render(request, 'yalladevelop/sitemap.html', {})

def privacy(request):
	return render(request, 'yalladevelop/privacy.html', {})

def terms(request):
	return render(request, 'yalladevelop/terms.html', {})

def test(request):
	return render(request, 'yalladevelop/111.html', {})