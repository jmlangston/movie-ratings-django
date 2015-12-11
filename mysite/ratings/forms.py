from django import forms
from django.contrib.auth.models import User

from .models import UserProfile

# resource: tangowithdjango.com chapter 8

class UserForm(forms.ModelForm):

	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'password')


# class UserProfileForm(forms.ModelForm):
	# class Meta:
		# model = UserProfile
