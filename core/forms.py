from django import forms
from core.models import Answer,Question

class QuestionForm(forms.Form):
    """
    question form
    """
    title = forms.CharField(label="Please Fill The Title")
    question = forms.CharField(widget=forms.Textarea(attrs={'cols': 80, 'rows': 20}),label="Fill The Question")
    
    def __init__(self,user,*args,**kwargs):
        super(QuestionForm,self).__init__(*args,**kwargs)
        self.user = user

    def save(self):
        data = self.cleaned_data
        str_title = data['title']
        str_question = data['question']
        q = Question(user = self.user,title=str_title,question=str_question)
        q.save()
        return q

class AnswerForm(forms.Form):
    """
    answer form.
    """
    answer = forms.CharField(widget=forms.Textarea(attrs={'cols': 80, 'rows': 20}))
    
    def __init__(self,user,question,*args,**kwargs):
        super(AnswerForm,self).__init__(*args,**kwargs)
        self.user = user
        self.question = question
        
    
    def save(self):
        data = self.cleaned_data
        str_answer = data['answer']
        answer = Answer(user=self.user,
                        question=self.question,
                        answer = str_answer)
        answer.save()
        return answer
