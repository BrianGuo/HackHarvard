from django.db import models

# Create your models here.
class Course(models.Model):


class FreeTime(models.Model):



class Profile(models.Model):
	
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)

	courses = models.ManyToManyField(Course)

	free_time = models.ForeignKey(FreeTime)

	resume_or_linkedin = models.URLField()

	bio = models.TextField()
