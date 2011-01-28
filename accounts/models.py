from django.db import models
from django.contrib.auth.models import User 
from projections.projects.models import Town

class UserProfile(models.Model):  
	user = models.ForeignKey(User, unique=True)
	town = models.ForeignKey('projects.Town')
	position = models.CharField(max_length=100)

	# view.py
    # user.get_profile().whatever
	# @login_required
	# def view_foo(request):
	#    url = request.user.profile.url

	def __str__(self):  
		# return "%s's profile" % self.user
		return '%s %s (%s)' % (self.user.first_name, self.user.last_name, self.town)  
	
	def full_name(self):
		return '%s %s' % (self.user.first_name, self.user.last_name)

	# def create_user_profile(sender, instance, created, **kwargs):  
	#	if created:  
	#		profile, created = UserProfile.objects.get_or_create(user=instance)  

	# post_save.connect(create_user_profile, sender=User)
	
	
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])