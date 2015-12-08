from django.db import models

class User(models.Model):
	email = models.CharField(max_length=100)
	password = models.CharField(max_length=15)
	age = models.IntegerField(default=0)
	zipcode = models.CharField(max_length=5)

	def __str__(self):
		return self.email

class Movie(models.Model):
	title = models.CharField(max_length=200)
	release_date = models.DateTimeField()
	imdb_url = models.CharField(max_length=200)

	def __str__(self):
		return self.title

class Rating(models.Model):
	user = models.ForeignKey(User)
	movie = models.ForeignKey(Movie)
	score = models.IntegerField(default=0)

	def __str__(self):
		return "Rating of %d for %s" % (self.score, self.movie)
