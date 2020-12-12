from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponsePermanentRedirect
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from ipware import get_client_ip
from typing import Callable

import json

from core.models import (
    Pool, Question, UserAnswer, AnswerOption, TeamsToken, PoolToken,
    TeamsTeam, TeamsChannel, TeamsUser, PoolAnswer
)
from core.decorators import (
    validate_pool_token, validate_teams_token, teams_tab_view
)
from core.teams_utils import app_manifest, TeamsMetadata
from core.answer_processing import save_answers


@method_decorator(csrf_exempt, 'dispatch')
class PoolView(DetailView):
    model = Pool

    @method_decorator(validate_pool_token)
    @method_decorator(teams_tab_view)
    def get(self, request, pk):
        pool = Pool.objects.get(pk=pk)
        questions = pool.questions.all()

        def delete_msteams_url_trash(key: str, value: str):
            if key.endswith('id'):
                return value.removeprefix('19:').split('@thread')[0]
            else:
                return value
        
        ms_teams_metadata = (
            (key, delete_msteams_url_trash(key, request.GET[key]))
            for key in request.GET if key.startswith('mst_')
        )

        context = {
            'pool_name': pool.name,
            'questions': questions,
            'token': request.GET['token'],
            'metadata': ms_teams_metadata
        }

        return render(request, "pool.html", context=context)

    @method_decorator(validate_pool_token)
    @method_decorator(teams_tab_view)
    def post(self, request, pk):
        pool = get_object_or_404(Pool, pk=pk)
        questions = pool.questions.all()

        metadata = TeamsMetadata(request.POST)

        pool_answer = PoolAnswer.objects.create(
            ip=get_client_ip(request)[0],
            pool_token=PoolToken.objects.get(token=request.POST['token']),
            teams_channel=metadata.channel,
            teams_user=metadata.user,
            pool=pool
        )

        save_answers(request.POST, pool, pool_answer, metadata)
        return HttpResponse('OK')


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
    build_url = lambda u: mark_safe(request.build_absolute_uri(u))
    token_str = str(pool_token.token)
    context = {
        'pool_token': token_str,
        'website_url': build_url('/'),
        'content_url': build_url(f'/pool/{pool_id}/?token={token_str}'),
        'display_name': 'Feedback service',
    }
    return render(request, 'teams-settings-save.html', context=context)


def teams_manifest(request):
    context = {
        'website_url': request.build_absolute_uri('/'),
        'privacy_url': request.build_absolute_uri('/teams/privacy/'),
        'tos_url': request.build_absolute_uri('/teams/tos/'),
        'configuration_url': request.build_absolute_uri('/teams/settings/auth/'),
        'valid_domains': [request.get_host()]
    }
    response = JsonResponse(app_manifest(context))
    response['Content-Disposition'] = (
        'attachment; filename=fs_teams_manifest.json'
    )
    return response


def root(request):
    return HttpResponsePermanentRedirect('/admin/')
