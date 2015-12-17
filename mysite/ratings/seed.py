from datetime import datetime
import json


def convert_reviewers():
	"""Converts reviewers seed data to JSON and writes it to a fixtures file - this way Django will know how to load it into the database."""

	seed_file = open("seed_data/u.user")
	seed_data = seed_file.read().split("\n")
	new_reviewers = []
	pk = 1
	for line in seed_data:
		reviewer_data = line.split("|")
		if reviewer_data == ['']:
			continue
		age = int(reviewer_data[1])
		zipcode = reviewer_data[4]
		new_reviewer = {
			"model": "ratings.Reviewer",
			"pk": pk,
			"fields": {
				"age": age,
				"zipcode": zipcode
			}
		}
		new_reviewers.append(new_reviewer)
		pk += 1
	json_reviewers = json.dumps(new_reviewers)
	fixture_file = open("fixtures/initial_data_reviewers.json", "w")
	fixture_file.write(json_reviewers)
	fixture_file.close()


def convert_movies():
	seed_file = open("seed_data/u.item")
	seed_data = seed_file.read().split("\n")
	new_movies = []
	pk = 1
	for line in seed_data:
		movie_data = line.split("|")
		if movie_data == ['']:
			continue	
		title = movie_data[1]
		formatted_title = title[:-7]
		release_date = movie_data[2]
		if release_date == '':
			release_date = '02-Aug-1989'	# handle movie with no release date	
		datetime_date = datetime.strptime(release_date, "%d-%b-%Y")
		iso_date = datetime_date.isoformat()
		imdb_url = movie_data[4]
		new_movie = {
			"model": "ratings.Movie",
			"pk": pk,
			"fields": {
				"title": formatted_title,
				"release_date": iso_date,
				"imdb_url": imdb_url
			}
		}
		new_movies.append(new_movie)
		pk += 1
	json_movies = json.dumps(new_movies)
	fixture_file = open("fixtures/initial_data_movies.json", "w")
	fixture_file.write(json_movies)
	fixture_file.close()


def convert_ratings():
	seed_file = open("seed_data/u.data")
	seed_data = seed_file.read().split("\n")
	new_ratings = []
	pk = 1
	for line in seed_data:
		rating_data = line.split("\t")
		if rating_data == ['']:
			continue
		reviewer_id, movie_id, score = int(rating_data[0]), int(rating_data[1]), int(rating_data[2])
		new_rating = {
			"model": "ratings.Rating",
			"pk": pk,
			"fields": {
				"reviewer_id": reviewer_id,
				"movie_id": movie_id,
				"score": score
			}
		}
		new_ratings.append(new_rating)
		pk += 1
	json_ratings = json.dumps(new_ratings)
	fixture_file = open("fixtures/initial_data_ratings.json", "w")
	fixture_file.write(json_ratings)
	fixture_file.close()


if __name__ == "__main__":

	convert_reviewers()
	convert_movies()
	convert_ratings()
