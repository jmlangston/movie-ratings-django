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


# def user_list(request):
# 	""" Displays a list of movie reviewers (users) """
# 	reviewer_list = Reviewer.objects.order_by('id')
# 	context = {'reviewer_list': reviewer_list}
# 	return render(request, 'ratings/reviewer_list.html', context)

class UserListView(generic.ListView):
	model = Reviewer
	template_name = 'ratings/user_list.html'


def user_details(request, reviewer_id):
	""" Displays information about a given movie reviewer (user) """
	reviewer = get_object_or_404(Reviewer, pk=reviewer_id)
	ratings = Rating.objects.filter(reviewer_id=reviewer_id)
	return render(request, 'ratings/user_details.html', {'reviewer': reviewer, 'ratings': ratings})

# class UserDetailView(generic.DetailView):
# 	model = Reviewer
# 	template_name = 'ratings/reviewer_details.html'


# def movie_list(request):
# 	""" Displays a list of movies """
# 	movie_list = Movie.objects.order_by('id')
# 	context = {'movie_list': movie_list}
# 	return render(request, 'ratings/movie_list.html', context)

class MovieListView(generic.ListView):
	model = Movie
	template_name = 'ratings/movie_list.html'


def movie_details(request, movie_id):
	""" Displays information about a given movie and options for reviewing the movie """

	movie = get_object_or_404(Movie, pk=movie_id)
	ratings = Rating.objects.filter(movie_id=movie_id)

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
	context = RequestContext(request)
	registered = False
	if request.method == "POST":
		user_form = UserForm(data=request.POST)
		if user_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()
			registered = True
		else:
			print user_form.errors
	else:
		user_form = UserForm()
	return render(request, 'ratings/register.html', {'user_form': user_form, 'registered': registered})


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
			else:
				return HttpResponse("Your Movie Ratings account is disabled.")
		else:
			print "Invalid login details: {0}, {1}".format(username, password)
			return HttpResponse("Invalid login.")

	else:
		return render(request, 'ratings/login.html')


def user_logout(request):
	logout(request) # won't throw an error if user wasn't logged in
	messages.add_message(request, messages.SUCCESS, "You have successfully logged out!")
	return redirect('ratings:index') # redirect to home page


def add_review(request, movie_id):	
	""" Add a new score for a movie by a reviewer """
	# save variables: new score, movie, score

	# look up UserProfile - if none, need to add
	# if user's first review / if there's no corresponding reviewer object
	# create new reviewer
	# create new UserProfile with reviewer_id and user_id
	# create new rating 
	# if they have already rated, they can update their rating
	
	score = request.POST['score']
	current_user = request.user
	movie = Movie.objects.get(id=movie_id)	

	try:
		user_profile = UserProfile.objects.get(user=current_user)
		reviewer = user_profile.reviewer
		messages.add_message(request, messages.SUCCESS, "REVIEWER FOUND")
	
	# except Exception:
	except UserProfile.DoesNotExist:
		reviewer = Reviewer.objects.create(username=current_user.username)
		# don't save while testing 
		# reviewer = Reviewer(username=current_user.username)

		userprofile = UserProfile.objects.create(user=current_user, reviewer=reviewer)
		# userprofile = UserProfile(user=current_user, reviewer=reviewer)

		messages.add_message(request, messages.SUCCESS, "REVIEWER %s ADDED" % userprofile.user.username)


	new_rating = Rating.objects.create(reviewer_id=reviewer, movie_id=movie, score=score)
	messages.add_message(request, messages.SUCCESS, "NEW RATING ADDED")
	return redirect('ratings:movie_details', movie.id)


def update_review(request, movie_id):
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

