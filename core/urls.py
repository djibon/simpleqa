
from django.conf.urls.defaults import *
urlpatterns = patterns('core.views',
    url(r'^$', 'home', name='core-home'),
    url(r'^questions', 'questions',name='core-questions'),
    url(r'^q/(?P<qid>[\d]+)/$', 'question',name='core-question'),
    url(r'^q/add/$', 'question_add',name='core-question-add'),
    url(r'^a/add/(?P<qid>[\d]+)/$', 'answer_add',name='core-answer-add'),
    url(r'^accounts/signup/$','signup',name='core-signup'),
    url(r'^vote/(?P<aid>[\d]+)/$','vote',name='core-vote'),
    url(r'^tag/(?P<tag_name>[\w\d\s]+)/$','tag',name='core-tag'),
    url(r'^profile/(?P<username>[\w\d\s\_\-]+)/$','profile',name='core-profile'),
    url(r'^profile/edit/(?P<username>[\w\d\s\-\_]+)/$','profile_edit',name='core-profile-edit'),
    url(r'^search/$','search',name='core-search')
)
