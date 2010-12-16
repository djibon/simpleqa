from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,authenticate
from django.shortcuts import render_to_response,get_object_or_404
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db.models import Count

from core.models import Question,Answer,Vote
from core.forms  import AnswerForm,QuestionForm

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
    #update view
    question.view = question.view + 1
    question.save()
    return render_to_response('core/question.html',
                              {'question':question},
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
            'form' : form
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
    request.user.message_set.create(message="Thanks For Vote")
    return HttpResponseRedirect(reverse('core-question',args=[answer.question.id]))
    
