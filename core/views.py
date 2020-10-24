from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.views.generic.detail import DetailView

from core.models import Pool


class PoolView(DetailView):
    queryset = Pool.objects.prefetch_related('questions')

    def get(self, request):
        pool = self.get_object()
        # Template generates here
        pass

    def post(self, request):
        pool = self.get_object()
        answer_options_to_create = []
        answers_to_create = []
        for q_id, answer in request.POST:
            pass
