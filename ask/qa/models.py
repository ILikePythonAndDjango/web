from django.db import models
from django.contrib.auth.models import User

class QuestionManager(models.Manager):

    def new(self):
        return self.order_by('-addet_ad')

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

    def __str__(self):
        return self.title

class Answer(models.Model):
    text = models.TextField()
    added_at = models.DateTimeField(blank=True, auto_now_add=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(User)

    def __str__(self):
        return "on " + str(self.question) + " from " + self.author.get_full_name()
