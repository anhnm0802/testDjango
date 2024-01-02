from django.db import models
from account.models import Account
# Create your models here.

class Position(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Candidate(models.Model):
    fullname = models.CharField(max_length=50)
    photo = models.ImageField(upload_to="candidates")
    bio = models.TextField()
    positions = models.ManyToManyField(Position, related_name='candidates')

    def __str__(self):
        return self.fullname


class Votes(models.Model):
    voter = models.ForeignKey(Account, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE,related_name='positionss')
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)