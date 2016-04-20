from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class BookmarkWord(models.Model):
    word = models.CharField(max_length=255)
    user = models.ForeignKey(User, null=True, blank=True)

    def __unicode__(self):
        return str(self.pk) + ": " + self.word

class SearchedWord(models.Model):
    word = models.CharField(max_length=255)

    def __unicode__(self):
        return str(self.pk) + ": " + self.word