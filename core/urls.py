
from django.conf.urls.defaults import *
urlpatterns = patterns('core.views',
    url(r'^$', 'home', name='core-home'),
    url(r'^questions', 'questions',name='core-questions'),
    url(r'^q/(?P<qid>[\d]+)/$', 'question',name='core-question'),
    url(r'^q/add/$', 'question_add',name='core-question-add'),
    url(r'^a/add/(?P<id>[\d]+)/$', 'answer_add',name='core-answer-add'),
    url(r'^accounts/signup/$','signup',name='core-signup'),
)
