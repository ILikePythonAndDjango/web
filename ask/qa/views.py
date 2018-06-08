from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage
from django.views.decorators.http import require_GET
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import User

from .models import Question, Answer

from .forms import AskForm, AnswerForm, LogInForm, SignUpForm

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
    if request.method == 'POST':
       form = AskForm(request.POST)
       form._user = request.user
       if form.is_valid():
           question = form.save()
           return HttpResponseRedirect(question.get_url())
    form = AskForm()
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
    answers = Answer.objects.sort().filter(question=question)
    if request.method == 'POST':
        form = AnswerForm(request.POST, initial={'question': question})
        form._user = request.user
        if form.is_valid():
            answer = form.save()
            return HttpResponseRedirect(question.get_url())
    form = AnswerForm(initial={'question': question})
    return render(request, 'question.html', {
        'question': question,
        'answers': answers,
        'form': form,
    })

def log_in(request):
    error = ''
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                error = u"You have inputed uncorrected login/password!"
                return render(request, 'login.html', {'error': error, 'form': form})
    form = LogInForm()
    return render(request, 'login.html', locals())

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect('/')
    form = SignUpForm()
    return render(request, 'signup.html', locals())  

def test(request, *args, **kwargs):
    return HttpResponse("OK")
