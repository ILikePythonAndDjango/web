from django import forms

from .models import Question, Answer
from django.contrib.auth.models import User

class LogInForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class SignUpForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def save(self):
        return User.objects.create_user(**self.cleaned_data)

class AskForm(forms.Form):
    title = forms.CharField(max_length=255)
    text = forms.CharField(widget=forms.Textarea)

    def save(self):
        self.cleaned_data['author'] = self._user
        return Question.objects.create(**self.cleaned_data)

class AnswerForm(forms.Form):

    text = forms.CharField(widget=forms.Textarea)
    question = forms.ModelChoiceField(Question.objects, widget=forms.HiddenInput)

    def save(self):
        self.cleaned_data['author'] = self._user
        return Answer.objects.create(**self.cleaned_data)

