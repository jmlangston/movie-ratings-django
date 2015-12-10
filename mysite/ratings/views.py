from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.models import User, UserManager
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect

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


def login_view(request):
	""" Login page """

	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password) # returns User object if valid, returns None if invalid
		if user is not None:
			if user.is_active:
				login(request, user) # add user to session
				messages.add_message(request, messages.SUCCESS, "You have successfully logged in!")
				return redirect('ratings:index') # redirect to home page
		else:
			return render(request, 'ratings/login.html') # TODO - add flash message re invalid credentials
	else:
		return render(request, 'ratings/login.html')


def register(request):
	""" Create a new user account """

	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']

		usermanager = UserManager()
		user = usermanager.create_user(username=username, password=password)
		# user = get_user_model().objects.create_user ... ???
		# user.save() # save new user in db
		login(request, user) # add user to session
		messages.add_message(request, messages.SUCCESS, "Thank you for registering!")
		return redirect('ratings:index')
	else:
		return render(request, 'ratings/register.html')


def logout_view(request):
	logout(request) # won't throw an error if user wasn't logged in
	messages.add_message(request, messages.SUCCESS, "You have successfully logged out!")
	return redirect('ratings:index') # redirect to home page
