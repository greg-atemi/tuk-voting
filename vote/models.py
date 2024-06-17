from datetime import datetime, timezone
from django.contrib.auth.models import User
from django.db import models

class Election(models.Model):
    election_name = models.CharField(max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True)
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    def __str__(self):
        return self.election_name

class Candidate(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    registration_number = models.CharField(max_length=10, default=None)
    email = models.EmailField(default="test@test.com")
    first_name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=10)
    votes = models.IntegerField(default=0)

    Male = 'Male'
    Female = 'Female'
    Other = 'Other'
    GENDER_CHOICES = [
        (Male, 'Male'),
        (Female, 'Female'),
        (Other, 'Other'),
    ]
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES)

    def __str__(self):
        return self.first_name

class Voter(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    registration_number = models.CharField(max_length=10, default=None)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, default=None)
    email = models.EmailField(default="test@test.com")
    first_name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=10)
    status = models.BooleanField(default=False)

    Male = 'Male'
    Female = 'Female'
    Other = 'Other'
    GENDER_CHOICES = [
        (Male, 'Male'),
        (Female, 'Female'),
        (Other, 'Other'),
    ]
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES)

    def __str__(self):
        return self.first_name
