#python manage.py shell

def generate_skills():
	from yalladevelop.models import Skill
	Skill.objects.bulk_create([Skill(name="Python"),Skill(name="Java"),Skill(name="C"),Skill(name="Ruby"),Skill(name="HTML"),Skill(name="PHP"),Skill(name="Perl"),Skill(name="ASP"),Skill(name="Adobe"),Skill(name="SQL")])

# Populate with projects

# UserProfile.objects.bulk_create([
# 	
# 	User(username="userOne",password="xxx",email="mruser1@gmail.com")
# 	UserProfile(name="User One",a=True,b=True,c=True),
# 	
# 	User(username="userTwo",password="xxx",email="mruser2@gmail.com")
# 	UserProfile(name="User Two"),
# 	
# 	User(username="userThree",password="xxx",email="mruser3@gmail.com")
# 	UserProfile(name="User Three",a=True),
# 	
# 	User(username="userFour",password="xxx",email="mruser4@gmail.com")
# 	UserProfile(name="User Four",f=True,g=True,h=True),
# 	
# 	User(username="userFive",password="xxx",email="mruser5@gmail.com")
# 	UserProfile(name="User Five",a=True,i=True,j=True,b=True),
# ])
# 
# 
# name = forms.CharField(max_length=200,help_text="First and Last name please.")
# email = forms.EmailField(help_text="Enter your email address",required=True)
# a = forms.BooleanField(label="Python, Django",required=False)
# b = forms.BooleanField(label="Java, Javascript",required=False)
# c = forms.BooleanField(label="C, C++, C#", required=False)
# d = forms.BooleanField(label="Ruby, Ruby on Rails",required=False)
# e = forms.BooleanField(label="HTML, CSS",required=False)
# f = forms.BooleanField(label="PHP",required=False)
# g = forms.BooleanField(label="Perl",required=False)
# h = forms.BooleanField(label="ASP & VBScript", required=False)
# i = forms.BooleanField(label="Adobe Photoshop, Illustrator",required=False)
# j = forms.BooleanField(label="SQL Databases",required=False)
# 
# 
