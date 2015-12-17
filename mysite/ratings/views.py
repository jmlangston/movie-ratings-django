from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.template import RequestContext
from django.views import generic

from .forms import UserForm
from .models import Movie, Rating, Reviewer, UserProfile


def index(request):
	""" Home page """
	return render(request, 'ratings/index.html')


class UserListView(generic.ListView):
	""" Displays a list of all users """
	template_name = 'ratings/user_list.html'
	context_object_name = 'custom_reviewer_list'

	def get_queryset(self):
		return Reviewer.objects.all().order_by('-id')


def user_details(request, reviewer_id):
	""" Displays information about a given movie reviewer """
	reviewer = get_object_or_404(Reviewer, pk=reviewer_id)
	ratings = Rating.objects.filter(reviewer_id=reviewer_id)
	return render(request, 'ratings/user_details.html', {'reviewer': reviewer, 'ratings': ratings})


class MovieListView(generic.ListView):
	""" Displays a list of all movies """
	template_name = 'ratings/movie_list.html'
	context_object_name = 'movies_alpha_order'

	def get_queryset(self):
		return Movie.objects.all().order_by('title')


def movie_details(request, movie_id):
	""" Displays information about a given movie and options for reviewing the movie. If a user is logged in, they have the option to add a review for the movie. If they have already rated the movie, they have the option to update their rating. If a user is not logged in, there will be a message indicating they can rate the movie if they log in. """

	movie = get_object_or_404(Movie, pk=movie_id)
	all_ratings_for_movie = list(Rating.objects.filter(movie_id=movie_id).order_by('reviewer_id'))
	ratings_with_username = []
	for rating in all_ratings_for_movie:
		if rating.reviewer_id.username != '':
			i = all_ratings_for_movie.index(rating)
			has_username = all_ratings_for_movie.pop(i)
			ratings_with_username.append(has_username)
	ratings = {'with_username': ratings_with_username, 'no_username': all_ratings_for_movie}
	try:
		current_user = request.user
		user_profile = UserProfile.objects.get(user=current_user)
		reviewer = user_profile.reviewer
		user_rating = Rating.objects.get(movie_id=movie_id, reviewer_id=reviewer)
		user_has_rated = True
	except Exception:
		user_rating = 'n/a'
		user_has_rated = False
	return render(request, 'ratings/movie_details.html', {'movie': movie, 'ratings': ratings, 'user_has_rated': user_has_rated, 'user_rating': user_rating})


def register(request):
	""" Register a new user """
	context = RequestContext(request)
	registered = False
	if request.method == "POST":
		user_form = UserForm(data=request.POST)
		if user_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()
			registered = True
			auth_user = authenticate(username=request.POST['username'], password=request.POST['password'])
			if auth_user:
				if auth_user.is_active:
					login(request, auth_user)
					messages.add_message(request, messages.SUCCESS, "Thank you for registering. You are logged in.")
					return redirect('ratings:index')
				else:
					return HttpResponse("Your Movie Ratings account is disabled.")
			else: 
				return HttpResponse("Could not authenticate.")
		else:
			return HttpResponse("Invalid login form.")
	else:
		user_form = UserForm()
		return render(request, 'ratings/register.html', {'user_form': user_form})


def user_login(request):
	""" Log in an existing user """
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
			else:
				return HttpResponse("Your Movie Ratings account is disabled.")
		else:
			print "Invalid login details: {0}, {1}".format(username, password)
			return HttpResponse("Invalid login.")

	else:
		return render(request, 'ratings/login.html')


def user_logout(request):
	""" Log out a user """
	logout(request) # won't throw an error if user wasn't logged in
	messages.add_message(request, messages.SUCCESS, "You have successfully logged out!")
	return redirect('ratings:index')


def add_review(request, movie_id):	
	""" Adds a new score for a movie by a reviewer. If the user has not reviewed any movies yet, this method will create UserProfile and Reviewer objects """
	
	score = request.POST['score']
	current_user = request.user
	movie = Movie.objects.get(id=movie_id)	
	try:
		user_profile = UserProfile.objects.get(user=current_user)
		reviewer = user_profile.reviewer
	except UserProfile.DoesNotExist:
		reviewer = Reviewer.objects.create(username=current_user.username)
		userprofile = UserProfile.objects.create(user=current_user, reviewer=reviewer)
	new_rating = Rating.objects.create(reviewer_id=reviewer, movie_id=movie, score=score)
	messages.add_message(request, messages.SUCCESS, "New movie rating added")
	return redirect('ratings:movie_details', movie.id)


def update_review(request, movie_id):
	""" Allows a user to update their rating for a movie they're already reviewed """ 
	updated_score = request.POST['updated_score']
	current_user = request.user
	movie = Movie.objects.get(id=movie_id)
	user_profile = UserProfile.objects.get(user=current_user)
	reviewer = user_profile.reviewer
	rating = Rating.objects.get(movie_id=movie, reviewer_id=reviewer)
	rating.score = updated_score
	rating.save()
	messages.add_message(request, messages.SUCCESS, "You have updated your rating for this movie")
	return redirect('ratings:movie_details', movie.id)

