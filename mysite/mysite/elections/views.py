from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Candidate, Poll, Choice
import datetime
# Create your views here.


def index(request):
    candidates = Candidate.objects.all()
    context = {'candidates' : candidates}
    return render(request, 'elections/index.html', context)


def areas(request, area):
    today = datetime.datetime.now()
    try:
        poll = Poll.objects.get(area = area, start_date__lte = today, end_date__gte=today)
        candidates = Candidate.objects.filter(area = area)
    except:
        poll = None
        candidates = None
    context = {'candidates' : candidates,
               'area' : area,
               'poll' : poll}
    return render(request, 'elections/area.html', context)

def polls(request, poll_id):
    poll = Poll.objects.get(id = poll_id)
    selection = request.POST['choice']

    try:
        choice = Choice.objects.get(poll = poll.id, candidate = selection)
        choice.votes += 1
        choice.save()
    except:
        choice = Choice(poll = poll.id, candidate = selection, votes=1)
        choice.save()
    return HttpResponseRedirect("/areas/{}/results".format(poll.area))

def results(request, area):
    candidates = Candidate.objects.filter(area=area)
    choice = Choice.objects.all()
    polls = Poll.objects.filter(area = area)
    poll_results = []
    for poll in polls:
        result = {}
        result['start_date'] = poll.start_date
        result['end_date'] = poll.end_date
        poll_results.append(result)
    context = {'candidates' : candidates,
               'area' : area,
               'poll_results' : poll_results
               }
    return render(request, 'elections/result.html', context)