from django import forms
from .models import Question, Answer

class AskForm(forms.Form):
    title = forms.CharField(max_length=255)
    text = forms.CharField(widget=forms.Textarea)

    def __init__(self, user, *args, **kwargs):
        self._user = user
        super(AskForm, self).__init__(*args, **kwargs)

    def clean(self):
        pass

    def save(self):
        self.cleaned_data['author'] = self._user
        question = Question(**self.cleaned_data)
        question.save()
        return question

class AnswerForm(forms.Form):

    text = forms.CharField(widget=forms.Textarea)
    question = forms.ModelChoiceField(Question.objects, widget=forms.HiddenInput)

    def __init__(self, user, *args, **kwargs):
        self._user = user
        super(AnswerForm, self).__init__(*args, **kwargs)

    def clean(self):
        pass

    def save(self):
        self.cleaned_data['author'] = self._user
        answer = Answer(**self.cleaned_data)
        answer.save()
        return answer

