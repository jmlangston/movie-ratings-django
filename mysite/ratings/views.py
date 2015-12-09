from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

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
