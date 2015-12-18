from django.contrib.auth.models import User
from django.db import models

import correlation

class Reviewer(models.Model):
	username = models.CharField(max_length=20)
	age = models.IntegerField(default=0)
	zipcode = models.CharField(max_length=5)

	def __str__(self):
		return "Reviewer number %s" % self.id

	def similarity(self, other_user):
		""" Returns Pearson rating comparing reviewer to other reviewer """
		user1_ratings = Rating.objects.filter(reviewer_id=self.id)
		user2_ratings = Rating.objects.filter(reviewer_id=other_user.id)
		ratings_dict = {}
		paired_ratings = []
		for u1_rating in user1_ratings:
			ratings_dict[u1_rating.movie_id_id] = u1_rating
		for u2_rating in user2_ratings:
			movie = u2_rating.movie_id_id
			if ratings_dict.get(movie):
				u1_rating = ratings_dict.get(movie)
				paired_ratings.append( (u1_rating.score, u2_rating.score) )
			else:
				continue
		if paired_ratings:
			return correlation.pearson(paired_ratings)
		else:
			return 0.0


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
		return "Rating of %d for %s" % (self.score, self.movie_id)


class UserProfile(models.Model):
	user = models.OneToOneField(User)
	reviewer = models.ForeignKey(Reviewer)

	def __str__(self):
		return self.user.username


if __name__ == "__main__":

	convert_reviewers()
	convert_movies()
	convert_ratings()
