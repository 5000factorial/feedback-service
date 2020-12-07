from django.test import TestCase, RequestFactory
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied

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
        correct_token = 'test_correct_token'
        validator = lambda token: token == correct_token
        for method in (self.request_factory.get, self.request_factory.post):
            decorator = decorators.validate_query_token(validator)
            decorated_view = decorator(self.view)
            correct_token_request = method(
                '/', {'token': correct_token}
            )
            incorrect_token_request = method(
                '/', {'token': 'incorect_token'})
            no_token_request = method('/')

            # Assert not raises
            resp = decorated_view(correct_token_request)

            with self.assertRaises(PermissionDenied):
                decorated_view(incorrect_token_request)

            with self.assertRaises(PermissionDenied):
                decorated_view(no_token_request)

    def test_validate_teams_token(self):
        pass

    def test_validate_pool_token(self):
        pass
