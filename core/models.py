from django.db import models as db
from django.contrib.auth.models import User
from django.db.models import Avg

from tagging.fields import TagField
from tagging.models import Tag

class Question(db.Model):
    """
    Question objects.
    """
    posted = db.DateTimeField(auto_now=True)
    question = db.TextField(max_length=100)
    user = db.ForeignKey(User)
    title = db.CharField(max_length=100)
    view = db.IntegerField(default=0)
    tags = TagField()

    def __unicode__(self):
        return self.title
    
    def save(self, force_insert=False, force_update=False, using=None):
        tags = ",".join(Tag.objects.get_for_object(self).values_list('name',flat=True))
        super(Question,self).save(force_insert,force_update,using)
        Tag.objects.update_tags(self,tags)
    

class Answer(db.Model):
    """
    Answers Object
    """
    posted = db.DateTimeField(auto_now=True)
    answer = db.TextField(max_length=100)
    question = db.ForeignKey(Question)
    user = db.ForeignKey(User)
    
    def __unicode__(self):
        return self.question.title +" "+self.answer
    
    def get_total_votes(self):
        return self.vote_set.all().count()
    
    def get_total_vote_score(self):
        point =  self.vote_set.aggregate(average_vote=(Avg('point')))['average_vote']
        return 0 if point==None else point

class Vote(db.Model):
    """
    Vote object
    """
    answer = db.ForeignKey(Answer)
    user   = db.ForeignKey(User)
    added =  db.DateTimeField(auto_now=True)
    point = db.IntegerField(default=0)

