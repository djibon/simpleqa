from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response,get_object_or_404
from django.template import RequestContext

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
    pass

def question(request,qid):
    """
    question details
    """
    pass

@login_required
def question_add(request):
    """
    add question form
    and handler form
    """
    pass

@login_required
def answer_add(request,qid):
    """
    add anser
    """
    pass
    
def signup(request):
    """
    signup
    """
