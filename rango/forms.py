from django.shortcuts import render

from django.http import HttpResponse
from rango.models import Category
from rango.models import Page
from django import forms
from django.contrib.auth.models import User
from rango.models import UserProfile
from rango.models import maxCharField
def index(request):
	category_list = Category.objects.order_by('-likes')[:5]
	page_list = Page.objects.order_by('-views')[:5]
	context_dict = {}
	context_dict['boldmessage'] ='Crunchy, creamy, cookie, candy, cupcake!'
	context_dict['categories'] = category_list
	context_dict['pages'] = page_list

	return render(request, 'rango/index.html', context=context_dict)


def about(request):
	context_dict = {'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!'}
	return render(request, 'rango/about.html', context=context_dict)

def show_category(request, category_name_slug):
	context_dict = {}
	try:
		category = Category.objects.get(slug=category_name_slug)
		pages = Page.objects.filter(category=category)
		context_dict['pages'] = pages
		context_dict['category'] = category

	except Category.DoesNotExist:
		context_dict['pages'] = None
		context_dict['category'] = None

	return render(request, 'rango/category.html', context=context_dict)


def show_page(request, page_name_slug):
	context_dict = {}
	try:
		pages = Page.objects.get(slug=category_name_slug)
		context_dict['pages'] = pages

	except Page.DoesNotExist:
		context_dict['pages'] = None

	return render(request, 'rango/page.html', context=context_dict)

class CategoryForm(forms.ModelForm):
	Category.name
	name = forms.CharField(max_length=maxCharField, help_text="Please enter the category name.")
	views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	slug = forms.CharField(widget=forms.HiddenInput(), required=False)

	class Meta:
		model = Category
		fields = ('name',)

class PageForm(forms.ModelForm):
	title = forms.CharField(max_length=maxCharField, help_text="Please enter the title of the page.")
	url = forms.URLField(max_length=200, help_text="Please enter the URL of the page.")
	views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	
	class Meta:
		model= Page
		# What fields do we want to include in our form?
	 	# This way we don't need every field in the model present.
		# Some fields may allow NULL values; we may not want to include them.
		# Here, we are hiding the foreign key.
		#32  we can either exclude the category field from the form,
		exclude = ('category',)
		# or specify the fields to include (don't include the category field).
		#fields = ('title', 'url', 'views')



class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields= ('website', 'picture',)