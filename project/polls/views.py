from django.core import serializers
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, loader
from django.utils import simplejson

from project.polls.models import Poll, Choice

def index(request):
    # return HttpResponse("Hello, World.")
    return render_to_response("index.html", {})

def list(request):
    latest_poll_list = Poll.objects.all().order_by("-pub_date")[:5]
    # t = loader.get_template("polls/index.html")
    # c = Context({"latest_poll_list" : latest_poll_list})
    # return HttpResponse(t.render(c))
    return render_to_response("polls/index.html", {"latest_poll_list" : latest_poll_list})

def detail(request, poll_id):
    # try:
    #     p = Poll.objects.get(pk = poll_id)
    # except Poll.DoesNotExist:
    #     raise Http404
    p = get_object_or_404(Poll, pk = poll_id)
    return render_to_response("polls/detail.html", {"poll" : p})

def results(request, poll_id):
    p = get_object_or_404(Poll, pk = poll_id)
    return render_to_response("polls/results.html", {"poll" : p})

def vote(request, poll_id):
    p = get_object_or_404(Poll, pk = poll_id)
    try:
        selected_choice = p.choice_set.get(pk = request.POST['choice'])
    except (KeyError, ValueError, Choice.DoesNotExist):
        return render_to_response("polls/detail.html", {
            "poll" : p,
            "error_message" : "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('project.polls.views.results', args = (p.id,)))

def json_dump(request):
    poll_list = Poll.objects.all().order_by("-pub_date")
    json_s = serializers.serialize("json", poll_list, ensure_ascii=False)
    return HttpResponse(json_s, mimetype='application/json')

def xml_dump(request):
    poll_list = Poll.objects.all().order_by("-pub_date")
    xml_s = serializers.serialize("xml", poll_list)
    return HttpResponse(xml_s, mimetype='text/xml')
