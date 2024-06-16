from django.contrib import admin
from vote.models import Voter, Election, Candidate

# Register your models here.

admin.site.register(Voter)
admin.site.register(Election)
admin.site.register(Candidate)
