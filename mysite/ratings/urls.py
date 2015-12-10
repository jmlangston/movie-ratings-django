from django.conf.urls import url

from . import views

urlpatterns = [
	# ex: /movieratings/
	url(r'^$', views.index, name='index'),
	# ex: /movieratings/users
	url(r'^users/$', views.user_list, name='user_list'),
	# ex: /movieratings/users/1
	url(r'^users/(?P<user_id>[0-9]+)/$', views.user_details, name='user_details'),
	url(r'^movies/$', views.movie_list, name='movie_list'),
	url(r'^movies/(?P<movie_id>[0-9]+)/$', views.movie_details, name='movie_details'),
	url(r'^login/$', views.login_view, name='login'),
	url(r'^logout/$', views.logout_view, name='logout')
]