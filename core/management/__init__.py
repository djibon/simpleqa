from django.db.models import signals
from django.conf import settings
from south import signals as south_signals

if "badge" in settings.INSTALLED_APPS:
    from badge import models 
    import badge
    def create_badges(app,**kwargs):
        if app != 'badge':
            return
        print 'create badges'
        models.create_badges("critic","Awarded when a registered user votes something down for the first time")
        models.create_badges("supporter","Awarded when a registered user votes something up for the first time")
        models.create_badges("student","Awarded once a registered user gets one of their questions voted up for the first time")
        models.create_badges("tumbleweed","Awarded when a registered user asks a question and the question receives no votes, answers, or comments.")
    
    south_signals.post_migrate.connect(create_badges)
else:
    print "Skipping creation of badges as badges app not found"
