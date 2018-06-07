from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage
from django.views.decorators.http import require_GET

from django.contrib.auth.models import User
from .models import Question, Answer

from .forms import AskForm, AnswerForm

def paginate(request, qs):

    '''
    paginate(request, qs) => tuple(paginator, page)
    This function paginates with all rules:
    1. Checks the validity of limit and page
    2. If function get uncorrect parameters then it raises exception Http404
    3. Function does within limit <= 100
    '''

    try:
        limit = int(request.GET.get('limit', 10))
    except ValueError:
        limit = 10

    if limit > 100:
        limit = 10

    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        raise Http404

    paginator = Paginator(qs, limit)

    try:
        page = paginator.page(page)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return paginator, page

def ask(request):
    user = User.objects.get(id=1)
    if request.method == 'POST':
       form = AskForm(user, request.POST)
       if form.is_valid():
           question = form.save()
           return HttpResponseRedirect(question.get_url())
    form = AskForm(user)
    return render(request, 'ask.html', locals())
          

@require_GET
def index(request):
    paginator, page = paginate(request, Question.objects.new())
    return render(request, "index.html", {
        'questions': page.object_list,
        'path': '/?page=',
        'paginator': paginator,
        'page': page,
    })

@require_GET
def popular(request):
    paginator, page = paginate(request, Question.objects.popular())
    return render(request, "index.html", {
        'questions': page.object_list,
        'path': '/popular/?page=',
        'paginator': paginator,
        'page': page,
    })

def get_question(request, pk):
    question = get_object_or_404(Question.objects, id=pk)
    answers = Answer.objects.filter(question=question)
    user = User.objects.get(id=1)
    if request.method == 'POST':
        form = AnswerForm(user, request.POST, initial={'question': question})
        if form.is_valid():
            answer = form.save()
            return HttpResponseRedirect(question.get_url())
    form = AnswerForm(user, initial={'question': question})
    return render(request, 'question.html', {
        'question': question,
        'answers': answers,
        'form': form,
    })

def test(request, *args, **kwargs):
    return HttpResponse("OK")
