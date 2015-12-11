from django.contrib import admin

from .models import Reviewer, Movie, Rating, UserProfile

admin.site.register(Reviewer)
admin.site.register(Movie)
admin.site.register(Rating)
admin.site.register(UserProfile)
