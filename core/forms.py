from django import forms
from core.models import Answer,Question
from tagging.models import Tag

class ProfileForm(forms.Form):
    """
    profile form
    """
    email = forms.EmailField(required=False)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    def __init__(self,user,*args,**kwargs):
        super(ProfileForm,self).__init__(*args,**kwargs)
        if user:
            self.user = user
            self.fields['email'].initial = self.user.email
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name

    def save(self):
        if not self.user:
            return None
        data = self.cleaned_data
        self.user.email = data['email']
        self.user.first_name = data['first_name']
        self.user.last_name = data['last_name']
        self.user.save()
        return self.user


class QuestionForm(forms.Form):
    """
    question form
    """
    title = forms.CharField(label="Please Fill The Title")
    question = forms.CharField(widget=forms.Textarea(attrs={'cols': 80, 'rows': 20}),label="Fill The Question")
    tags = forms.CharField(label="Please Fill the tags",required=False,help_text="Tags separated by comma")

    def __init__(self,user,*args,**kwargs):
        super(QuestionForm,self).__init__(*args,**kwargs)
        self.user = user

    def save(self):
        data = self.cleaned_data
        str_title = data['title']
        str_question = data['question']
        str_tags= data['tags']
        tags = str_tags.split(',')
        
        q = Question(user = self.user,title=str_title,question=str_question)
        q.save()
        for t in tags:
            Tag.objects.add_tag(q,t.strip())
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
