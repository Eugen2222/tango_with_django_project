from django.shortcuts import render

from django.http import HttpResponse
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from rango.forms import PageForm
from django.shortcuts import redirect
from django.urls import reverse
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime



def index(request):
	category_list = Category.objects.order_by('-likes')[:5]
	page_list = Page.objects.order_by('-views')[:5]
	context_dict = {}
	context_dict['boldmessage'] ='Crunchy, creamy, cookie, candy, cupcake!'
	context_dict['categories'] = category_list
	context_dict['pages'] = page_list
	visitor_cookie_handler(request)



	response = render(request, 'rango/index.html', context=context_dict)


	return response


def about(request):
	context_dict = {'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!'}

	context_dict['visits'] = request.session['visits']
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


def add_category(request):
	if request.user.is_authenticated:
		form = CategoryForm()

		if request.method == 'POST':
			form = CategoryForm(request.POST)
			
			if form.is_valid():

				cat = form.save(commit = True)
				print(cat, cat.slug)
				return redirect('/rango/')

			else:
				print(form.errors)

		return render(request, 'rango/add_category.html', {'form': form})
	else:
		return redirect(reverse('rango:login'))


def add_page(request, category_name_slug):
	if request.user.is_authenticated:
		try:
			category = Category.objects.get(slug=category_name_slug)
		except Category.DoesNotExist:
			category = None
		
		if category is None:
			return redirect('/rango/')

		form = PageForm()

		if request.method == 'POST':
			form = PageForm(request.POST)

			if form.is_valid():
				if category:
					page = form.save(commit = False)
					page.category=category
					page.views = 0
					page.save()

				return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))

			else:
				print(form.errors)

		context_dict = {'form':form, 'category':category}

		return render(request, 'rango/add_page.html', context=context_dict)
	else:
		return redirect(reverse('rango:login'))


def register(request):

	registered = False

	if request.method == 'POST':
		user_form = UserForm(request.POST)
		profile_form = UserProfileForm(request.POST)

		if user_form.is_valid() and profile_form.is_valid():

			user = user_form.save()

			user.set_password(user.password)
			user.save()

		# Now sort out the UserProfile instance.
		# Since we need to set the user attribute ourselves,
		# we set commit=False. This delays saving the model
		# until we're ready to avoid integrity problems.
			profile = profile_form.save(commit=False)
			profile.user = user

		# Did the user provide a profile picture?
		# If so, we need to get it from the input form and
		#put it in the UserProfile model.
			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']
		
			profile.save()
			registered = True
		else:
			print(user_form.errors, profile_form.errors)
	else:

		user_form = UserForm()
		profile_form = UserProfileForm()

	return render(request, 'rango/register.html', 
					context = {'user_form': user_form,
								'profile_form': profile_form,
								'registered': registered})

def user_login(request):
	#if the request is a HTTP POST, try to pull out the relevant information.
	if request.method == 'POST':
		#Gather the username and password provided by the user.
		#This information is obtained from the login form.
		#We use request.POST.get('<variable>') as opposed
		#to request.POST['<variable>'], because the
		#request.POST.get('<variable>') returns None if the
		#value does not exist, while request.POST['<variable>']
		#will raise a KeyError exception.
		username = request.POST.get('username')
		password = request.POST.get('password')
		
		#Use Django machinery to attempt to see if the username/password
		#combination is valid - a User object is required if it is.
		user = authenticate(username = username, password = password)

		#If we have a User object, the details are correct.
		#If None (Python's way of representing the absence of a value), no
		#user with matching credentials was found.
		if user:
			#Is the account active? It could have been disabled.
			if user.is_active:
				#If the account is valid and active, we can log the user in.
				#We'll send the user back to homepage.
				login(request,user)
				return redirect(reverse('rango:index'))
			else:
				#An inactive account was used - no logging in
				return HttpResponse("Your Rango account is disable.")
		else:
			#Bad login details were provided. So we can't log the user in
			print(f"Invalid login details: {username}, {password}")
			return HttpResponse("Invalid login details supplied")
	#The request is not a HTTP POST, so display the login form.
	#The scenario would most likely be a HTTP GET
	else:
		#No context variables to pass to the template system, hence the
		#blank dictionary object.
		return render(request, 'rango/login.html')
		

@login_required
def restricted(request):
	return render(request, 'rango/restricted.html')


@login_required
def user_logout(request):
	#Since we know the user is logged in, we can now just log them out.
	logout(request)
	#Take the user back to the homepage
	return redirect(reverse('rango:index'))


def visitor_cookie_handler(request):
	#Get the number of visitor to the site
	visits = int(get_server_side_cookie(request, 'visits', '1'))

	last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
	last_visit_time = datetime.strptime(last_visit_cookie[:-7],'%Y-%m-%d %H:%M:%S')

	if (datetime.now() - last_visit_time).days>0:
		visits = visits + 1
		request.session['last_visit'] = str(datetime.now())
	else:
		request.session['last_visit'] = last_visit_cookie

	request.session['visits'] = visits

def get_server_side_cookie(request, cookie, default_val = None):
	val = request.session.get(cookie)
	if not val:
		val = default_val
	return val
