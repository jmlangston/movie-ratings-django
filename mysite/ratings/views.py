from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.models import User, UserManager
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, render_to_response, redirect
from django.template import RequestContext

# from .forms import UserForm, UserProfileForm
from .forms import UserForm
from .models import User, Movie, Rating


def index(request):
	return render(request, 'ratings/index.html')


def user_list(request):
	""" Displays a list of users """
	user_list = User.objects.order_by('id')
	context = {'user_list': user_list}
	return render(request, 'ratings/user_list.html', context)


def user_details(request, user_id):
	""" Displays information about a given user """
	
	user = get_object_or_404(User, pk=user_id)
	return render(request, 'ratings/user_details.html', {'user': user})

def movie_list(request):
	""" Displays a list of movies """
	movie_list = Movie.objects.order_by('id')
	context = {'movie_list': movie_list}
	return render(request, 'ratings/movie_list.html', context)


def movie_details(request, movie_id):
	""" Displays information about a given movie """

	movie = get_object_or_404(Movie, pk=movie_id)
	return render(request, 'ratings/movie_details.html', {'movie': movie})


# def login_view(request):
# 	""" Login page """

# 	if request.method == "POST":
# 		username = request.POST['username']
# 		password = request.POST['password']
# 		user = authenticate(username=username, password=password) # returns User object if valid, returns None if invalid
# 		if user is not None:
# 			if user.is_active:
# 				login(request, user) # add user to session
# 				messages.add_message(request, messages.SUCCESS, "You have successfully logged in!")
# 				return redirect('ratings:index') # redirect to home page
# 		else:
# 			return render(request, 'ratings/login.html') # TODO - add flash message re invalid credentials
# 	else:
# 		return render(request, 'ratings/login.html')


def user_login(request):
	context = RequestContext
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user:
			if user.is_active:
				login(request, user)
				messages.add_message(request, messages.SUCCESS, "You have successfully logged in!")
				return redirect('ratings:index')
				# return redirect('ratings:index')
			else:
				return HttpResponse("Your Movie Ratings account is disabled.")
		else:
			print "Invalid login details: {0}, {1}".format(username, password)
			return HttpResponse("Invalid login.")

	else:
		# return render_to_response('ratings:login', {}, context)
		return render(request, 'ratings/login.html')


def register(request):
	context = RequestContext(request)
	registered = False
	if request.method == "POST":
		user_form = UserForm(data=request.POST)
		# profile_form = UserProfileForm(data=request.POST)

		# if user_form.is_valid() and profile_form.is_valid():
		if user_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()

			# profile = profile_form.save(commit=False)
			# profile.user = user 

			# profile.save()

			registered = True
			
			# messages.add_message(request, messages.SUCCESS, "Thank you for registering!")
			# return redirect('ratings:index')
		
		else:
			print user_form.errors
			# print user_form.errors, profile_form.errors
			# messages.add_message(request, messages.ERROR, "Invalid login. Please enter again.")
			# return redirect('ratings:register')

	else:
		user_form = UserForm()
		# profile_form = UserProfileForm()
		
	# return render_to_response(
		# 'ratings/register.html', 
		# {'user_form': user_form, 'registered': registered},
		# context)

	return render(request, 'ratings/register.html', {'user_form': user_form, 'registered': registered})


def user_logout(request):
	logout(request) # won't throw an error if user wasn't logged in
	messages.add_message(request, messages.SUCCESS, "You have successfully logged out!")
	return redirect('ratings:index') # redirect to home page


# @login_required
# def user_logout(request):
	# logout(request)
	# return redirect('ratings:index')

