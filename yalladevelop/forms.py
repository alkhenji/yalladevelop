from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from yalladevelop.models import Skill, UserProfile

class UserCreateForm(UserCreationForm):
	name = forms.CharField(max_length=200,help_text="First and Last name please.")
	email = forms.EmailField(help_text="Enter your email address",required=True)
	a = forms.BooleanField(label="Python, Django",required=False)
	b = forms.BooleanField(label="Java, Javascript",required=False)
	c = forms.BooleanField(label="C, C++, C#", required=False)
	d = forms.BooleanField(label="Ruby, Ruby on Rails",required=False)
	e = forms.BooleanField(label="HTML, CSS",required=False)
	f = forms.BooleanField(label="PHP",required=False)
	g = forms.BooleanField(label="Perl",required=False)
	h = forms.BooleanField(label="ASP & VBScript", required=False)
	i = forms.BooleanField(label="Adobe Photoshop, Illustrator",required=False)
	j = forms.BooleanField(label="SQL Databases",required=False)
	
	class Meta:
		model = User
		fields = ("name","username","password1","password2","email")
		
	def save(self, commit=True):
		user = super(UserCreateForm, self).save(commit=False)
		user.email = self.cleaned_data["email"]
		fullName = self.cleaned_data["name"]
		a = self.cleaned_data["a"]
		b = self.cleaned_data["b"]
		c = self.cleaned_data["c"]
		d = self.cleaned_data["d"]
		e = self.cleaned_data["e"]
		f = self.cleaned_data["f"]
		g = self.cleaned_data["g"]
		h = self.cleaned_data["h"]
		i = self.cleaned_data["i"]
		j = self.cleaned_data["j"]
		A = Skill.objects.get(id=1)
		B = Skill.objects.get(id=2)
		C = Skill.objects.get(id=3)
		D = Skill.objects.get(id=4)
		E = Skill.objects.get(id=5)
		F = Skill.objects.get(id=6)
		G = Skill.objects.get(id=7)
		H = Skill.objects.get(id=8)
		I = Skill.objects.get(id=9)
		J = Skill.objects.get(id=10)
		
		if commit:
			user.save()
			userProfile = UserProfile(user=user, name=fullName)
			userProfile.save()
			if a: userProfile.skill.add(A)
			if b: userProfile.skill.add(B)
			if c: userProfile.skill.add(C)
			if d: userProfile.skill.add(D)
			if e: userProfile.skill.add(E)
			if f: userProfile.skill.add(F)
			if g: userProfile.skill.add(G)
			if h: userProfile.skill.add(H)
			if i: userProfile.skill.add(I)
			if j: userProfile.skill.add(J)
		return user