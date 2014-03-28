''' This will be the Controller of the Application. Examples below. '''

# Urls and HttpResponses
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, render_to_response

# User forms
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Permission
from yalladevelop.forms import *

# Authentication and Users
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.core.context_processors import csrf
from django.template import RequestContext

# Models
from yalladevelop.models import Project, Skill, UserProfile, Like

# Mailer
from django.core.mail import send_mail

# Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Other Imports
import random


# -------------------- Parameters Function -------------------------
# Function returns a dictionary of the variables
def getVariables(request,dictionary={}):
	user = request.user
	logged_in = request.user.is_authenticated()
	not_logged_in = not logged_in
	admin = request.user.is_staff
	if logged_in and not admin:
		user_is_company = UserProfile.objects.get(user=user).is_company
		user_profile = UserProfile.objects.get(user=user)
	elif admin:
		user_is_company = False
		user_profile = False
	else: #not logged in
		user_is_company = False
		user_profile = False
	if dictionary:
		dictionary['user'] = user
		dictionary['logged_in'] = logged_in
		dictionary['not_logged_in'] = not logged_in
		if logged_in and not admin:
			user_is_company = UserProfile.objects.get(user=user).is_company
			dictionary['is_company'] = user_is_company
		return dictionary
	else:
		return {'user':user,'logged_in':logged_in,'not_logged_in':not_logged_in,'is_company':user_is_company, 'user_profile': user_profile}


def rankings(request):
	d = getVariables(request,dictionary={'page_name': "Rankings"})
	top_users = UserProfile.objects.filter(is_company=False).order_by('-points')[:10]
	top_companies = UserProfile.objects.filter(is_company=True).order_by('-points')[:10]
	
	top_projects = Project.objects.order_by('-likes')[:10]
	
	d['top_users'] = top_users
	d['top_companies'] = top_companies
	d['top_projects'] = top_projects
	
	return render(request,'yalladevelop/rankings.html',d)


def index(request):
	d = getVariables(request,dictionary={'page_name': "Home"})
	return render(request, 'yalladevelop/index.html', d)

@csrf_exempt #login required
def addProject(request):
	d = getVariables(request)
	if d['is_company']:
		return redirect('/')
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

	
def showProject(request,project_id=-1):
	d = getVariables(request,dictionary={'page_name': "Browse Projects"})
	if project_id > 0:
		project = Project.objects.filter(id=project_id)
		if project:
			project = project[0]
			d['page_name'] = "Project: %s" % project.name
			d['project'] = project
			d['owner'] = User.objects.get(id=project.user_id).username
			d['progress'] = int(project.money_collected/project.target_money)
			if True: # should be if logged in
				user = request.user
				projectLiked = Like.objects.filter(project_id=project.id,user_id=user.id)
				if projectLiked:
					d['liked'] = True
				else:
					d['liked'] = False
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
	if profile_id == str(1):
		if request.user.is_staff:
			return redirect('/admin')
		else:
			return redirect('/')
	elif profile_id > 1:	
		userAccount = User.objects.get(id=profile_id)
		userProfile = UserProfile.objects.get(user=userAccount)
		if userProfile:
			skills = userProfile.skill.all()
			d['userAccount'] = userAccount
			d['userProfile'] = userProfile
			d['page_name'] = "%s's Profile" % userProfile.name
			d['my_page'] = False
			if request.user.id == userAccount.id:
				d['my_profile'] = True
			else:
				d['my_profile'] = False
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
	return render(request, "yalladevelop/signup.html", {'form': form,'usersignup':True})

@csrf_exempt
def signup_company(request):
	if request.method == 'POST':
		form = CompanyCreateForm(request.POST)
		if form.is_valid():
			new_user = form.save()
			new_user = authenticate(username=request.POST['username'],password=request.POST['password1'])
			login(request, new_user)
			url = reverse('index')
			return HttpResponseRedirect(url)
	else:
		form = CompanyCreateForm()
	return render(request, "yalladevelop/signup.html", {'form': form,'usersignup':False})

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


def randomPasswordGenerator():
	alphabet = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*"
	password_length = 10
	new_password = ""
	for i in range(password_length):
		c = random.randrange(len(alphabet))
		new_password += alphabet[c]
	return new_password


def forgotPassword(request):
	d = getVariables(request)
	if request.method == "POST":
		form = ForgotForm(request.POST)
		if form.is_valid():
			# fetch the username by email
			email = form.cleaned_data['email']
			user = User.objects.filter(email=email)
			if user:
				user = user[0]			
				new_password = randomPasswordGenerator()
				user.set_password(new_password)
				subject = "YallaDevelop - Password Reset"
				message = "Password have been reset, your new password is %s" % new_password
				sender = "noreply@yalladevelop.com"
				recipients = ['al.khenji@gmail.com']
				send_mail(subject,message,sender,recipients)
				return HttpResponseRedirect('/')
		form = ForgotForm()
		d['form'] = form
		return render(request, 'yalladevelop/forgotpassword.html', d)
	else:
		form = ForgotForm()
		d['form'] = form
	return render(request, "yalladevelop/forgotpassword.html", d)

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

def userorcompany(request):
	d = getVariables(request)
	return render(request, 'yalladevelop/userorcompany.html', {})


@login_required
def update_company(request):
	d = getVariables(request)
	u = request.user
	up = d['user_profile']
	
	
@login_required
def update_user(request):
	pass

@login_required
def profileSettings(request):
	d = getVariables(request)
	if request.method == "POST":
		if d['user_profile'].is_company:
			form = CompanyUpdateForm(request.POST)
		else: #if user
			form = UserUpdateForm(request.POST)
		if form.is_valid():
			form.update(d)
			return redirect("/profile/" + str(request.user.id))
	else:
		u = request.user
		up = d['user_profile']
		if d['user_profile'].is_company:
			d['form'] = CompanyUpdateForm(initial={'name':up.name,'email':u.email})
		else:
			initial = {'name':up.name,'email':u.email}
			letter = lambda i: "abcdefghijklmnopqrstuvwxyz"[i-1] #takes a number, returns character
			for skill in Skill.objects.all():
				if skill not in up.skill.all():
					initial[letter(skill.id)] = False
				else:
					initial[letter(skill.id)] = True
			d['form'] = UserUpdateForm(initial=initial)
	return render(request, 'yalladevelop/profile_settings.html', d)


# def profileSettings(request):
# 	d = getVariables(request)
# 	d['skills'] = Skill.objects.all()
# 	d['user_skills'] = d['user_profile'].skill.all()
# 	return render(request, 'yalladevelop/profile_settings.html', d)
# 
# 
# @login_required
# def save_settings(request):
# 	if request.method == 'POST':
# 		data = request.POST
# 		print data
# 		if request.user.check_password(request.POST['password1']):
# 			name = data['firstname']
# 			new_pass1 = data['password2']
# 			new_pass2 = data['password3']
# 			print 'x'+name+'x',new_pass1,new_pass2
# 			# password correct, update settings
# 		else:
# 			return redirect('/profile_settings/')
# 	else:
# 		return redirect('/')

# -------------------- Functions -------------------------
# def postComment(request,image_id=1):
# 	name = request.user.username
# 	comment = request.GET['comment']
# 	gallery_owner = int(Entry.objects.get(id=image_id).userId)
# 	userID = request.user.id
# 	c = Comment(username=name, comment=comment, imageId=image_id, userId=userID)
# 	c.save()
# 	url = "/webgallery/user/"+str(gallery_owner)+"/image/"+str(image_id)+"/"
# 	return HttpResponseRedirect(url)

@login_required
def likeProject(request,project_id):
	like = Like.objects.filter(project_id=project_id,user_id=request.user.id)
	project = Project.objects.filter(id=project_id)
	if not project:
		return HttpResponseRedirect("/")
	else:
		project = project[0]
		user = request.user
		liked = Like.objects.filter(project_id=project.id,user_id=user.id)		
		if not liked:
			newLike = Like(project_id=project.id,user_id=user.id)
			newLike.save()
			project.likes += 1
			project.save()
		url = '/project/%s' % str(project.id)
		return HttpResponseRedirect(url) # return to project page
