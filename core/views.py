from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,authenticate
from django.contrib.auth.models import User
from django.contrib.comments.models import Comment
from django.shortcuts import render_to_response,get_object_or_404
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db.models import Count

from badge.models import Badge,UserBadge
from core.models import Question,Answer,Vote
from core.forms  import AnswerForm,QuestionForm,ProfileForm
from core.search_utils import *
from tagging.models import Tag,TaggedItem

def home(request):
    """
    home handler
    """
    return render_to_response('core/index.html',
                              {},
                              context_instance= RequestContext(request))

def questions(request):
    """
    List of questions
    """
    
    context = {}
    questions = Question.objects.all().order_by('-posted')
    value = request.GET.get('sort','id')
    direction = request.GET.get('dir','up')

    context['questions'] = _sort(value,direction,questions)
    return render_to_response('core/questions.html',
                              context,
                              context_instance=RequestContext(request))
def _sort(value,direction,qs):
    point  = '-' if direction=='-' else ""
    str_order = "%s%s" % (point,value)

    if value == 'answer':
        return qs.annotate(answer=Count('answer')).order_by(str_order)
    
    return qs.order_by(str_order)

def question(request,qid):
    """
    question details
    """
    question = get_object_or_404(Question,id=qid)
    question.view = question.view + 1
    question.save()
    tags = Tag.objects.get_for_object(question)
    if question.view > 1:
        answer_count = question.answer_set.all().count()
        comments_count = Comment.objects.for_model(question).count()
        
        if answer_count == 0 and comments_count == 0:
            badge = Badge.objects.get(name='tumbleweed')
            UserBadge.objects.add_badge_to_user(question.user,badge)

    return render_to_response('core/question.html',
                              {'question':question,
                               'next':reverse('core-question',args=[question.id])},
                              context_instance=RequestContext(request))

@login_required
def question_add(request):
    """
    add question form
    and handler form
    """
    if request.method == 'POST':
        form = QuestionForm(request.user,request.POST)
        if form.is_valid():
            question = form.save()
            request.user.message_set.create(message="Thanks for submit the question")
            return HttpResponseRedirect(reverse('core-question',args=[question.id]))
    else:
        form = QuestionForm(request.user)
        
    return render_to_response("core/question_edit.html", 
            {
            'form' : form,
            },context_instance=RequestContext(request))

@login_required
def answer_add(request,qid):
    """
    add answer
    """
    question = get_object_or_404(Question,id=qid)
    if request.method == 'POST':
        form = AnswerForm(request.user,question,request.POST)
        if form.is_valid():
            form.save()
            request.user.message_set.create(message="Thanks for answer the question")
            return HttpResponseRedirect(reverse('core-question',args=[question.id]))
    else:
        form = AnswerForm(request.user,question)

    return render_to_response("core/answer.html", 
            {
            'form' : form,
            'question':question
            },context_instance=RequestContext(request))

    
def signup(request):
    """
    signup
    """
    if request.user.is_authenticated():
        return render_to_response(
            'core/index.html',
            {},
            context_instance=RequestContext(request)
        )

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(username=new_user.username, password=form.cleaned_data['password1'])
            login(request,new_user)
            new_user.message_set.create(message="Thanks For Register, Enjoy")
            return HttpResponseRedirect(reverse('core-home'))
    else:
        form = UserCreationForm()

    return render_to_response("registration/register.html", {
        'form' : form
    },context_instance=RequestContext(request))


@login_required
def vote(request,aid):
    """
    votes handler
    redirect to question page.
    """
    answer = get_object_or_404(Answer,id=aid)
    if answer.user == request.user:
         request.user.message_set.create(message="Sorry you cannot vote your own answer")
         return HttpResponseRedirect(reverse('core-question',args=[answer.question.id]))
   
    user = request.user
    #tupple
    vote = Vote.objects.get_or_create(answer=answer,user=user)[0]
    is_up = request.GET.get('dir','down')
    point = -1
    if is_up=='up':
        point = 1
    elif is_up=='down':
        point = -1
    
    vote.point = point
    vote.save()
    #create a badge
    if point == 1:
        badge = Badge.objects.get(name='supporter')
        UserBadge.objects.add_badge_to_user(user,badge)
    elif point == -1:
        badge = Badge.objects.get(name='critic')
        UserBadge.objects.add_badge_to_user(user,badge)
    
    badge = Badge.objects.get(name='student')
    UserBadge.objects.add_badge_to_user(answer.user,badge)
    request.user.message_set.create(message="Thanks For Vote")
    return HttpResponseRedirect(reverse('core-question',args=[answer.question.id]))
    
def tag(request,tag_name):
    """
    tags
    """
    context = {}
    tag = get_object_or_404(Tag,name=tag_name)
    questions = TaggedItem.objects.get_by_model(Question,[tag,])
    value = request.GET.get('sort','id')
    direction = request.GET.get('dir','up')

    context['questions'] = _sort(value,direction,questions)
    return render_to_response('core/questions.html',
                              context,
                              context_instance=RequestContext(request))

def profile(request,username):
    """
    profile page
    context:
    - user
    - question
    - answer
    - badges
    - user
    """
    user = get_object_or_404(User,username=username)
    is_user = user == request.user
    questions = Question.objects.filter(user =user)
    answers = Answer.objects.filter(user=user)
    return render_to_response('core/profile.html',
                              {'user':user,
                               'is_user':is_user,
                               'questions':questions,
                               'answers':answers},
                              context_instance=RequestContext(request))

def profile_edit(request,username):
    """
    profile edit
    context:
    - form
    """
    user = get_object_or_404(User,username=username)
    if request.method == 'POST':
        form = ProfileForm(user,request.POST)
        if form.is_valid():
            form.save()
            request.user.message_set.create(message="Profile has been updated")
            return HttpResponseRedirect(reverse('core-profile',args=[user.username]))
    else:
        form = ProfileForm(user)

    return render_to_response('core/profile_edit.html',
                              {'form':form},
                              context_instance = RequestContext(request))

def search(request):
    """
    search page
    context:
    - questions
    """
    str_query = request.GET.get('q',None)
    if str_query == None:
        return HttpResponseRedirect(reverse('core-questions'))
    context = {}
    qs = get_search_query(str_query,['name'])
    tags = Tag.objects.filter(qs)
    questions = TaggedItem.objects.get_by_model(Question,tags)
    value = request.GET.get('sort','id')
    direction = request.GET.get('dir','up')
    context['questions'] = _sort(value,direction,questions)
    context['search'] = '&q=%s' % str_query
    return render_to_response('core/questions.html',
                              context,
                              context_instance=RequestContext(request))
