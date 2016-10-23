from django.db import models
from django.conf import settings

# Create your models here.


class Course(models.Model):
    department = models.CharField(max_length=30)
    number = models.CharField(max_length=4)
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.department + " " + self.number


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    courses = models.ManyToManyField(Course)

    resume_or_linkedin = models.URLField()

    bio = models.TextField()

    def __str__(self):
        return self.first_name + " " + self.last_name


class DateDuration(models.Model):
    profile = models.ForeignKey(Profile)

    DATE_CHOICES = (
        ('M', "Monday"),
        ('T', "Tuesday"),
        ('W', "Wednesday"),
        ('R', "Thursday"),
        ('F', "Friday"),
        ('S', "Saturday"),
        ('U', "Sunday")
    )
    date = models.CharField(max_length=1, choices=DATE_CHOICES)
    time_start = models.TimeField()
    time_end = models.TimeField()

    in_proposed_group = models.BooleanField()


class Group(models.Model):
    course = models.ForeignKey(Course)
    members = models.ManyToManyField(Profile)
    name = models.CharField(max_length=30)

    meeting_time = models.OneToOneField(DateDuration)
    location = models.CharField(max_length=50)
