from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.views.decorators.http import require_GET

from .models import Question, Answer

@require_GET
def index(request):
    questions = Question.objects.new()
    page = request.GET.get('page', 1)
    limit = request.GET.get('limit', 10)
    paginator = Paginator(questions, limit)
    page = paginator.page(page)
    return render(request, "index.html", {
        'questions': page.object_list,
    })

@require_GET
def popular(request):
    questions = Question.objects.popular()
    page = request.GET.get('page', 1)
    limit = request.GET.get('limit', 10)
    paginator = Paginator(questions, limit)
    page = paginator.page(page)
    return render(request, "index.html", {
        'questions': page.object_list,
    })

@require_GET
def get_question(request, pk):
    question = get_object_or_404(Question.objects, id=pk)
    answers = Answer.objects.filter(question=question)
    return render(request, 'question.html', {
        'question': question,
        'answers': answers,
    })

def test(request, *args, **kwargs):
    return HttpResponse("OK")
