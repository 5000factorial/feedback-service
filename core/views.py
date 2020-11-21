from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from collections import defaultdict
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied
from django.utils.safestring import mark_safe
from ipware import get_client_ip
from typing import Callable

import json

from core.models import (
    Pool, Question, UserAnswer, AnswerOption, User, TeamsToken, PoolToken
)
from core.decorators import (
    validate_pool_token, validate_teams_token, teams_tab_view
)


class PoolView(DetailView):
    model = Pool

    @method_decorator(validate_pool_token)
    @method_decorator(teams_tab_view)
    def get(self, request, pk):
        ip = get_client_ip(request)
        pool = Pool.objects.get(pk=pk)
        questions = pool.questions.all()

        result = defaultdict(list)
        for item in questions:
            result[item] = [el.text for el in AnswerOption.objects.filter(question=item)]
        return render(request, "pool.html", context={"pool_name": pool.name, "result": dict(result)})

    def post(self, request, pk):
        ip = get_client_ip(request)
        question_pks = set(request.POST.keys())
        question_pks.remove('csrfmiddlewaretoken')
        questions = Question.objects.filter(pk__in=question_pks)

        user_answers_to_create = []
        user, _ = User.objects.get_or_create(username='test_user')

        for question in questions:
            answer = request.POST[str(question.id)]
            if question.category == Question.CLOSED:
                user_answers_to_create.append(
                    UserAnswer(user=user, question=question, option_id=answer)
                )
            elif question.category == Question.OPEN:
                answer_option = AnswerOption.objects.get_or_create(
                    question=question,
                    text=answer.lower()
                )
                user_answers_to_create.append(
                    UserAnswer(user=user, question=question, option_id=answer_option.id)
                )

        UserAnswer.objects.bulk_create(user_answers_to_create)
        return HttpResponse('OK')


# def teams_view_decorator(func):
#     """ Sets Content-Security-Policy header and legacy X-Content-Security-Policy for MS Teams """
    
#     content_security_policy = 'frame-ancestors teams.microsoft.com *.teams.microsoft.com *.skype.com'
    
#     def wrapper(request, *args, **kwargs):
#         response = func(request, *args, **kwargs)
#         response['Content-Security-Policy'] = response['X-Content-Security-Policy'] = content_security_policy
#         return response
    
#     return wrapper


# def token_validation_decorator(validator: Callable[[str], bool]):
#     """ Checks token form query parameter with validator function """
#     def decorator(func):
#         def wrapper(request, *args, **kwargs):
#             if validator(request.GET.get('token')):
#                 return func(request, *args, **kwargs)
#             else:
#                 raise PermissionDenied('Invalid token')
#         return wrapper
#     return decorator


# teams_token_validator_decorator = token_validation_decorator(
#     lambda token: TeamsToken.objects.filter(token=token).exists()
# )


# pool_token_validator_decorator = token_validation_decorator(
#     lambda pool_token: PoolToken.objects.filter(token=pool_token).exists()
# )


@teams_tab_view
def teams_settings_auth(request):
    return render(request, 'teams-settings-auth.html')


@teams_tab_view
@validate_teams_token
def teams_settings_pool(request):
    context = {
        'pools': Pool.objects.all(),
        'teams_token': request.GET['token']
    }
    return render(request, 'teams-settings-pool.html', context=context)


@teams_tab_view
@validate_teams_token
def teams_settings_save(request):
    pool_id = request.GET['pool']
    pool_token = PoolToken.objects.create(pool_id=request.GET['pool'])
    build_url = lambda u: mark_safe(build_absolute_uri(u))
    context = {
        'pool_token': str(pool_token),
        'website_url': build_url('/'),
        'content_url': build_url(f'/teams/pool/{pool_id}/?token={pool_token}'),
        'display_name': 'Feedback service',
    }
    return render(request, 'teams-settings-save.html', context=context)


def teams_manifest(request):
    return HttpResponse('')
