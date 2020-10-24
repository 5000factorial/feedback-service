from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.views.generic.detail import DetailView

from core.models import Pool


class PoolView(DetailView):
    model = Pool

    def get(self, request):
        pool = self.object
        # Template generates here
        pass

    def post(self, request):
        pass
