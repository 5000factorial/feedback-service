from django.test import TestCase, RequestFactory
from django.http import HttpResponse

import core.models as models
import core.decorators as decorators


class DecoratorTestCase(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()
        self.pool = models.Pool.objects.create(name='test')
        self.pool_token = models.PoolToken.objects.create(pool=self.pool)
        self.teams_token = models.TeamsToken.objects.create()
        
        def test_view(*args, **kwargs):
            return HttpResponse()

        self.view = test_view

    def test_teams_tab_view(self):
        decorated_view = decorators.teams_tab_view(self.view)
        response = decorated_view(self.request_factory.get('/'))
        self.assertEqual(decorators.MS_TEAMS_CONTENT_SECURITY_POLICY,
                         response['Content-Security-Policy'])
        self.assertEqual(decorators.MS_TEAMS_CONTENT_SECURITY_POLICY,
                         response['X-Content-Security-Policy'])            

    def test_validate_query_token(self):
        pass

    def test_validate_teams_token(self):
        pass

    def test_validate_pool_token(self):
        pass
