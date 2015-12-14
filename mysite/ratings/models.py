from django.contrib.auth.models import User
from django.db import models

class Reviewer(models.Model):
	# email = models.CharField(max_length=100)
	# password = models.CharField(max_length=15)

	username = models.CharField(max_length=20)
	age = models.IntegerField(default=0)
	zipcode = models.CharField(max_length=5)

	def __str__(self):
		return "Reviewer number %s" % self.id


class Movie(models.Model):
	title = models.CharField(max_length=200)
	release_date = models.DateTimeField()
	imdb_url = models.CharField(max_length=200)

	def __str__(self):
		return self.title


class Rating(models.Model):
	# TODO - remove id from column names
	reviewer_id = models.ForeignKey(Reviewer)
	movie_id = models.ForeignKey(Movie)
	score = models.IntegerField(default=0)

	def __str__(self):
		return "Rating of %d for %s" % (self.score, self.movie)


class UserProfile(models.Model):
	user = models.OneToOneField(User)

	reviewer = models.ForeignKey(Reviewer)

	def __str__(self):
		return self.user.username
