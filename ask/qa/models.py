from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

class QuestionManager(models.Manager):

    def new(self):
        return self.order_by('-added_at')

    def popular(self):
        return self.order_by('-rating')

class Question(models.Model):

    objects = QuestionManager()

    title = models.CharField(max_length=255)
    text = models.TextField()
    added_at = models.DateTimeField(blank=True, auto_now_add=True)
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(User)
    likes = models.ManyToManyField(User, related_name='likes_set')

    def get_url(self):
        return reverse("question", kwargs={"pk": self.id})

    def __str__(self):
        return self.title

class AnswerManager(QuestionManager):

    def sort(self):
        return self.order_by('-id')

class Answer(models.Model):

    objects = AnswerManager()

    text = models.TextField()
    added_at = models.DateTimeField(blank=True, auto_now_add=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(User)

    def get_url(self):
        return self.question.get_url()

    def __str__(self):
        return "Answer from {} at {}.".format(self.author.username, self.added_at)
