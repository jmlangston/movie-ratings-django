from django.conf.urls import url

from . import views

urlpatterns = [
	# ex: /movieratings/
	url(r'^$', views.index, name='index'),
	# ex: /movieratings/users
	url(r'^users/$', views.UserListView.as_view(), name='user_list'),
	# ex: /movieratings/users/1
	url(r'^users/(?P<reviewer_id>[0-9]+)/$', views.user_details, name='user_details'),
	# url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetailView.as_view(), name='user_details'),
	url(r'^movies/$', views.MovieListView.as_view(), name='movie_list'),
	url(r'^movies/(?P<movie_id>[0-9]+)/$', views.movie_details, name='movie_details'),
	# url(r'^movies/(?P<pk>[0-9]+)/$', views.MovieDetailView.as_view(), name='movie_details'),
	url(r'^login/$', views.user_login, name='login'),
	url(r'^logout/$', views.user_logout, name='logout'),
	url(r'^register/$', views.register, name='register')
]