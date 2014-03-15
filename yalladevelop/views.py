''' This will be the Controller of the Application. Examples below. '''

# Urls and HttpResponses
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, render_to_response

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

# Models
from yalladevelop.models import Project, Skill, UserProfile
from yalladevelop.forms import UserCreateForm, ContactForm, AddForm

# Mailer
from django.core.mail import send_mail

# Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# -------------------- Parameters Function -------------------------
# Function returns a dictionary of the variables
def getVariables(request,dictionary={}):
	user = request.user
	logged_in = request.user.is_authenticated()
	not_logged_in = not logged_in
	if dictionary:
		dictionary['user'] = user
		dictionary['logged_in'] = logged_in
		dictionary['not_logged_in'] = not logged_in
		return dictionary
	else:
		return {'user':user,'logged_in':logged_in,'not_logged_in':not_logged_in}


def index(request):
	d = getVariables(request,dictionary={'page_name': "Home"})
	return render(request, 'yalladevelop/index.html', d)


@csrf_exempt #login required
def addProject(request):
	d = getVariables(request)
	d['page_name'] = "Add Project"
	if request.method == "POST":
		form = AddForm(request.POST)
		if form.is_valid():
			name = form.cleaned_data['project_name']
			description = form.cleaned_data['description']
			money = form.cleaned_data['target_money']
			p = Project(name=name,user_id=request.user.id,target_money=money,description=description)
			p.save()
			url = '/project/%s' % str(p.id)
			return HttpResponseRedirect(url) # return to new project page
		else:
			form = AddForm()
			d['form'] = form
			return render(request, 'yalladevelop/addproject.html', d)
			# return HttpResponseRedirect('/addproject') # return to new project page
		return render(request, 'yalladevelop/addproject.html', d)
	else:
		form = AddForm()
		d['form'] = form
	return render(request, "yalladevelop/addproject.html", d)

# def showProject(request,project_id):
# 	d = getVariables(request)
# 	d['page_name'] = 'Browser Projects'
# 	project = Project.objects.filter(id=project_id)
# 	if profile:
# 		project = project[0] 
# 		owner = User.objects.filter(id=project.user_id)[0]
# 		page_name = "Project: %s" % project.name
# 		d['page_name'] = page_name
# 		return render(request,'yalladevelop/project.html', d)
# 	else:
# 		return render(request, 'yalladevelop/404.html')
	
def showProject(request,project_id=-1):
	d = getVariables(request,dictionary={'page_name': "Browse Projects"})
	if project_id > 0:
		project = Project.objects.filter(id=project_id)
		if project:
			project = project[0]
			d['page_name'] = "Project: %s" % project.name
			d['project'] = project
			d['owner'] = User.objects.get(id=project.user_id).username
			return render(request,'yalladevelop/project.html', d)
		else:
			return render(request, 'yalladevelop/404.html')
	elif project_id == -1:
		projects = Project.objects.all()
		d['projects'] = projects
		return render(request, 'yalladevelop/404.html')
	else:
		return render(request, 'yalladevelop/404.html')


def showProfile(request,profile_id=-1):
	d = getVariables(request,dictionary={'page_name': "Browse Profiles"})
	print "xxxxxxx: "+str(profile_id)
	if profile_id == str(1):
		print "ssss"
		return redirect('/admin')

	elif profile_id > 1:	
		userAccount = User.objects.get(id=profile_id)
		userProfile = UserProfile.objects.get(user=userAccount)
		if userProfile:
			skills = userProfile.skill.all()
			d['userAccount'] = userAccount
			d['userProfile'] = userProfile
			d['page_name'] = "%s's Profile" % userProfile.name
			return render(request,'yalladevelop/profile.html', d)
		else:
			return render(request, 'yalladevelop/404.html')
	elif profile_id == -1:
		return render(request, 'yalladevelop/allprofiles.html',d)
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
	d = getVariables(request)
	return render(request, 'yalladevelop/about.html', d)
	
def contact(request):
	d = getVariables(request)
	if request.method == "POST":
		form = ContactForm(request.POST)
		if form.is_valid():
			subject = form.cleaned_data['subject']
			message = form.cleaned_data['message']
			sender = form.cleaned_data['sender']
			cc_myself = form.cleaned_data['cc_myself']
			recipients = ['al.khenji@gmail.com']
			if cc_myself:
				recipients.append(sender)
			send_mail(subject,message,sender,recipients)
			return HttpResponseRedirect('/')
		else:
			form = ContactForm()
			d['form'] = form
		return render(request, 'yalladevelop/contact.html', d)
	else:
		form = ContactForm()
		d['form'] = form
	return render(request, "yalladevelop/contact.html", d)
	
def allprojects(request):
	d = getVariables(request)
	projects = Project.objects.all()
	paginator = Paginator(projects, 2) # Show 25 projects per page
	page = request.GET.get('page')
	try:
		projects = paginator.page(page)
	except PageNotAnInteger:
		projects = paginator.page(1)
	except EmptyPage:
		projects = paginator.page(paginator.num_pages)
	d['projects'] = projects
	return render_to_response('yalladevelop/allprojects.html',d)
	
def explore(request):
	d = getVariables(request)
	projects = Project.objects.all()
	paginator = Paginator(projects, 2) # Show 25 projects per page
	page = request.GET.get('page')
	try:
		projects = paginator.page(page)
	except PageNotAnInteger:
		projects = paginator.page(1)
	except EmptyPage:
		projects = paginator.page(paginator.num_pages)
	d['projects'] = projects
	return render_to_response('yalladevelop/explore.html',d)

def faq(request):
	d = getVariables(request)
	return render(request, 'yalladevelop/faq.html', d)

def help(request):
	d = getVariables(request)
	return render(request, 'yalladevelop/help.html', d)
	
def privacy(request):
	d = getVariables(request)
	return render(request, 'yalladevelop/privacy.html', d)

def sitemap(request):
	d = getVariables(request)
	return render(request, 'yalladevelop/sitemap.html', d)

def privacy(request):
	d = getVariables(request)
	return render(request, 'yalladevelop/privacy.html', {})

def terms(request):
	d = getVariables(request)
	return render(request, 'yalladevelop/terms.html', {})

def test(request):
	d = getVariables(request)
	return render(request, 'yalladevelop/111.html', {})

def dhelp(request):
	return render(request,'yalladevelop/components.html')

	
	
	
# -------------------- Functions -------------------------
# def postComment(request,image_id=1):
# 	name = request.user.username
# 	comment = request.GET['comment']
# 	gallery_owner = int(Entry.objects.get(id=image_id).userId)
# 	userID = request.user.id
# 	c = Comment(username=name, comment=comment, imageId=image_id, userId=userID)
# 	c.save()
# 	
# 	url = "/webgallery/user/"+str(gallery_owner)+"/image/"+str(image_id)+"/"
# 	return HttpResponseRedirect(url)
	
	








	