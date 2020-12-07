from django.test import TestCase

import core.models as models

class DecoratorTestCase(TestCase):
    def setUp(self):
        self.pool = models.Pool.objects.create('test')
        self.pool_token = models.PoolToken.objects.create()
        self.teams_token = models.TeamsToken.objects.create()

    def test_teams_tab_view(self):
        pass

    def test_validate_query_token(self):
        pass

    def test_validate_teams_token(self):
        pass

    def test_validate_pool_token(self):
        pass