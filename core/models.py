from django.db import models as db
from django.contrib.auth.models import User

class Question(db.Model):
    """
    Question objects.
    """
    posted = db.DateTimeField(auto_now=True)
    question = db.TextField(max_length=100)
    user = db.ForeignKey(User)
    title = db.CharField(max_length=100)

    def __unicode__(self):
        return self.title

class Answer(db.Model):
    """
    Answers Object
    """
    posted = db.DateTimeField(auto_now=True)
    answer = db.TextField(max_length=100)
    question = db.ForeignKey(Question)
    user = db.ForeignKey(User)
