from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.views.generic.detail import DetailView
from collections import defaultdict

from core.models import Pool, Question, UserAnswer, AnswerOption, User


class PoolView(DetailView):
    model = Pool

    def get(self, request, pk):
        pool = Pool.objects.get(pk=pk)
        questions = pool.questions.all()

        result = defaultdict(list)
        for item in questions:
            result[item] = [el.text for el in AnswerOption.objects.filter(question=item)]
        return render(request, "pool.html", context={"pool_name": pool.name, "result": dict(result)})

    def post(self, request, pk):
        question_pks = set(request.POST.keys())
        question_pks.remove('csrfmiddlewaretoken')
        questions = Question.objects.filter(pk__in=question_pks)

        user_answers_to_create = []
        user = User.objects.get_or_create(username='test_user')

        for question in questions:
            answer = request.POST[question.id]
            if question.type == Question.CLOSED:
                user_answers_to_create.append(
                    UserAnswer(user=user, question=question, option_id=answer)
                )
            elif question.type == Question.OPEN:
                answer_option = AnswerOption.objects.get_or_create(
                    question=question,
                    text=answer.lower()
                )
                user_answers_to_create.append(
                    UserAnswer(user=user, question=question, option_id=answer_option.id)
                )

        UserAnswer.objects.bulk_create(user_answers_to_create)
        return HttpResponse('OK')
