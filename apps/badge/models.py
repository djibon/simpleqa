from django.db import models
from django.contrib.auth.models import User


class Badge(models.Model):
    name = models.CharField(blank=False,null=False,editable=False,max_length=512)
    label = models.CharField(blank=True,null=True,max_length=512)

    def __unicode__(self):
        return "%s-%s" % (self.name,self.label)

class UserBadgeManager(models.Manager):
    def add_badge_to_user(self,user,badge):
        """
        add badge to user.
        if user already have that badge, we leave it alone.
        """
        user_badge,created = self.get_or_create(user=user,badge=badge)
        if created:
            us = UserBadgeMessage(userbadge=user_badge)
            us.save()

        return user_badge

    def get_user_for_badge(self,badge):
        """
        get users from badge
        """
        self.filter(badge=badge).values_list(user,flat=True)
        
    def get_badge_for_user(self,user):
        """
        get badge from user.
        """
        self.filter(user=user).values_list(badge,flat=True)

class UserBadge(models.Model):
    user = models.ForeignKey(User)
    badge = models.ForeignKey(Badge)
    objects = UserBadgeManager()
    
    def __unicode__(self):
        return self.user.username+" "+self.badge.name

class UserBadgeMessage(models.Model):
    userbadge = models.ForeignKey(UserBadge)
    display   = models.BooleanField(default=False)



def create_badges(name,label,verbosity=1):
    """
    create/edit badges
    """
    try:
        badge = Badge.objects.get(name=name)
        if badge.label != label:
            badge.label = label
            badge.save()
            if verbosity > 1:
                print "Update %s badge" % name
    except  Badge.DoesNotExist:
        Badge(name=name,label=label).save()
        if verbosity > 1:
            print "Create % badge" % name
