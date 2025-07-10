from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Candidate(models.Model):
    name = models.CharField(max_length=100)
    party = models.CharField(max_length=100)
    image = models.ImageField(upload_to='candidates/', blank=True, null=True)  # optional
    vote_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.party})"


class Vote(models.Model):
    voter = models.OneToOneField(User, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.voter.username} voted for {self.candidate.name}"


