from django.http import HttpResponseRedirect
# from django.views.generic import ListView

from .models import Questions, Choice
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic


def IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'


    def get_queryset(self):
        """Return the last five published questions."""
        return Questions.objects.order_by('-pub_date')[:5]


def detail(request, question_id):

    # try:
    #     question = Questions.objects.get(pk=question_id)
    # except Questions.DoesNotExist:
    #     raise Http404("Questions does not exists")
    # return HttpResponse("You're looking at questions %s." % question_id)

    question = get_object_or_404(Questions, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Questions, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Questions, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(
                reverse(
                    'polls:results',
                    args=(question.id,)
                )
        )
