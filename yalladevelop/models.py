#Database Models
''' This will be the database model '''

from django.db import models
from django import forms
from django.contrib.auth.models import User

class Skill(models.Model):
	# id built in
	'''
	a = "Python, Django"
	b = "Java, Javascript"
	c = "C, C++, C#"
	d = "Ruby, Ruby on Rails"
	e = "HTML, CSS"
	f = "PHP"
	g = "Perl"
	h = "ASP & VBScript"
	i = "Adobe Photoshop, Illustrator"
	j = "SQL Databases"
	'''
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=200)
	def __unicode__(self):
		return self.name
	
		
class UserProfile(models.Model):
	# firstName Already Built in
	# lastName Already Built in
	# email Already built in
	# password already built in
	# is_staff - Can access admin site?
	# is_active - Designates whether this user is active or not
	is_premium = models.BooleanField(default=False)
	is_company = models.BooleanField(default=False)
	skill = models.ManyToManyField(Skill)
	user = models.ForeignKey(User, unique=True)
	name = models.CharField(max_length=200)
	def __unicode__(self):
		return self.name

class Project(models.Model):
	user_id = models.IntegerField() # can be used to change owner of project later
	name = models.CharField(max_length=200)
	date_published = models.DateField(auto_now_add=True)
	date_completed = models.DateField(null=True)
	likes = models.IntegerField(default=0)
	target_money = models.IntegerField(null=False)
	money_collected = models.IntegerField(default=0)
	description = models.CharField(max_length=200)
	completed = models.BooleanField(default=False)
	def __unicode__(self):
		return self.name
