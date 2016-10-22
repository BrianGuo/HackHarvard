from django.db import models

# Create your models here.


class Course(models.Model):
    department = models.CharField(max_length=30)
    number = models.CharField(max_length=4)
    title = models.CharField(max_length=30)


	def __str__(self):
		return self.department + " " + self.number


class FreeTime(models.Model):
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()


class Profile(models.Model):

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    courses = models.ManyToManyField(Course)

    resume_or_linkedin = models.URLField()

    bio = models.TextField()

class FullProfile(models.Model):

    profile = models.OneToOneField(Profile)
    free_time = models.ManyToManyField(FreeTime)



