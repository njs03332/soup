from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.forms import UserCreationForm
from .models import Event, Article, Issue, Memo
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
from calendar import monthrange
from django.http import HttpResponseRedirect
from django.urls import reverse



now = datetime.datetime.now()

# Create your views here.
def temp(request):
    year = now.year
    month = now.month
    return redirect('/calendar/' + str(year) + str(month))

class CalendarView(LoginRequiredMixin, ListView):
    login_url = '/accounts/login/'
    template_name = 'newsdiary/calendar.html'
    context_object_name = 'events'

    def get_queryset(self):
        return Event.objects.filter(datetime__year=self.year(), datetime__month=self.month())

    def day_events(self):
        day_events = [[]]
        events = self.get_queryset()
        for i in range(1,monthrange(self.year(), self.month())[1]+1):
            v = []
            for e in events.filter(datetime__day=i):
                v.append(e)
            day_events.append(v)
        return day_events

    def month(self):
        if self.kwargs['pk'] >= 100000:
            return int(self.kwargs['pk'] % 100)
        else:
            return int(self.kwargs['pk'] % 10)

    def year(self):
        if self.kwargs['pk'] >= 100000:
            return int(self.kwargs['pk'] / 100)
        else:
            return int(self.kwargs['pk'] / 10)

    def days(self):
        return range(1,monthrange(self.year(), self.month())[1]+1)
    
    def before(self):
        return int(str(self.year()) + str(self.month()-1))

    def after(self):
        return int(str(self.year()) + str(self.month()+1))

    def weekday(self):
        #print(datetime(year=self.year(), month=self.month(), day=1).weekday())
        return datetime.datetime(self.year(), self.month(), 1).weekday()

    def saturday(self):
        ret = []
        for day in self.days():
            if day % 7 == 6 - self.weekday():
                ret.append(day)
        return ret
        
    def last_weekday(self):
        return datetime.datetime(self.year(), self.month(), monthrange(self.year(), self.month())[1]).weekday()

    def today(self):
        return datetime.datetime(2019,4,11).day

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'newsdiary/article/article.html'
    context_variable_name = 'article'

    def first_article(self):
        return Article.objects.first().id

    def next_article(self):
        return Article.objects.first().id + 1

class PreviewView(LoginRequiredMixin, ListView):
    login_url = '/accounts/login/'
    template_name = 'newsdiary/preview.html'
    context_object_name = 'events'

    def get_queryset(self):
        events = Event.objects.filter(title="WTO 판결") | Event.objects.filter(title="브렉시트") | Event.objects.filter(title="한국당 이미선 고발")
        return events

    def other_events(self):
        return Event.objects.filter(title="바른미래당 회의")

    def year(self):
        return datetime.datetime.today().year

    def month(self):
        return datetime.datetime.today().month

    def day(self):
        return datetime.datetime(2019,4,11).day

class ReviewView(LoginRequiredMixin, ListView):
    login_url = '/accounts/login/'
    template_name = 'newsdiary/review.html'
    context_object_name = 'articles'

    def get_queryset(self):
        # 오늘 기사 중에, 사용자가 팔로우하고 있는 일정에 대한 기사들
        # today = Article.objects.filter(created_at__date=datetime.date.today())
        # return today.filter(event__followers=self.request.user)
        return Article.objects.filter(title="후쿠시마 수산물 계속 못 들어온다…한국, WTO 분쟁서 승소")

    def other_articles(self):
        # today = Article.objects.filter(created_at__date=datetime.date.today())
        # return today.exclude(event__followers=self.request.user)
        return Article.objects.filter(title="임신중지 입법…기간·사유 제한으로 논의 좁히면 안 돼") | Article.objects.filter(title="유럽 증시, 브렉시트 연기에 투자심리 호전 상승 마감...런던만 약보합")

    def year(self):
        return datetime.datetime.today().year

    def month(self):
        return datetime.datetime.today().month

    def day(self):
        return datetime.datetime(2019,4,12).day

def follow(request, pk):
    event = Event.objects.get(id=pk)
    event.followers.add(request.user)
    event.save()
    event.issue.followers.add(request.user)
    event.save()
    return HttpResponseRedirect(request.GET['next'])

def unfollow(request, pk):
    event = Event.objects.get(id=pk)
    event.followers.remove(request.user)
    event.save()
    return HttpResponseRedirect(request.GET['next'])

class CreateMemoArticleView(LoginRequiredMixin, CreateView):
    login_url = '/accounts/login/'
    model = Memo
    fields = ['title', 'content']
    template_name = 'newsdiary/memo/new_article_memo.html'

    def form_valid(self, form):
        form.instance.article = Article.objects.get(pk=self.kwargs['pk'])
        form.instance.user = self.request.user
        return super().form_valid(form)

    def article(self):
        return Article.objects.get(pk=self.kwargs['pk'])

    def get_success_url(self):
        return reverse('article', kwargs={'pk': self.kwargs['pk']})

class CreateMemoIssueView(LoginRequiredMixin, CreateView):
    login_url = '/accounts/login/'
    model = Memo
    fields = ['title', 'content']
    template_name = 'newsdiary/memo/new_issue_memo.html'

    def form_valid(self, form):
        form.instance.issue = Issue.objects.get(pk=self.kwargs['pk'])
        form.instance.user = self.request.user
        return super().form_valid(form)

    def issue(self):
        return Issue.objects.get(pk=self.kwargs['pk'])

    def get_success_url(self):
        return reverse('memo_issue', args=[self.kwargs['pk']])

class MemoListView(LoginRequiredMixin, ListView):
    login_url = '/accounts/login/'
    template_name = 'newsdiary/memo/memos.html'
    context_object_name = 'memos'

    def get_queryset(self):
        return self.request.user.memos.all()

    # def other_issues(self):
    #     return Issue.objects.exclude(followers=self.request.user)

class IssueListView(LoginRequiredMixin, ListView):
    login_url = '/accounts/login/'
    template_name = 'newsdiary/issue/my_issues.html'
    context_object_name = 'issues'

    def get_queryset(self):
        issues = Issue.objects.filter(followers=self.request.user)
        for memo in self.request.user.memos.all():
            if memo.article:
                if memo.article.issue:
                    issues |= Issue.objects.filter(pk=memo.article.issue.pk)
                elif memo.article.event:
                    issues |= Issue.objects.filter(pk=memo.article.event.issue.pk)
            elif memo.issue:
                issues |= Issue.objects.filter(pk=memo.issue.pk)
        return issues

class MemoIssueListView(LoginRequiredMixin, ListView):
    login_url = '/accounts/login/'
    template_name = 'newsdiary/memo/memo_issue.html'
    context_object_name = 'memos'

    def get_queryset(self):
        return self.request.user.memos.filter(issue=Issue.objects.get(pk=self.kwargs['pk']))

    def issue(self):
        return Issue.objects.get(pk=self.kwargs['pk'])

    def event_memos(self):
        return self.request.user.memos.filter(article__issue=self.issue()) | self.request.user.memos.filter(article__event__issue=self.issue())

class MemoDetailView(LoginRequiredMixin, DetailView):
    login_url = '/accounts/login/'
    model = Memo
    template_name = 'newsdiary/memo/memo.html'
    context_variable_name = 'memo'

