import uuid
from django.test import TestCase, RequestFactory
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied

import core.models as models
import core.decorators as decorators
from core.answer_processing import save_answers
from core.teams_utils import TeamsMetadata


class DecoratorTestCase(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()
        self.pool = models.Pool.objects.create(name='test')
        self.pool_token = models.PoolToken.objects.create(pool=self.pool)
        self.teams_token = models.TeamsToken.objects.create()
        self.incorrect_uuid_token = uuid.uuid4()

        self.assertNotEqual(self.pool_token.token, self.incorrect_uuid_token)
        self.assertNotEqual(self.teams_token.token, self.incorrect_uuid_token)
        
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
        decorated_view = decorators.validate_teams_token(self.view)
        correct_token_request = self.request_factory.get(
            '/', {'token': self.teams_token.token}
        )
        incorrect_token_request = self.request_factory.get(
            '/', {'token': self.incorrect_uuid_token}
        )

        # Assert not raises
        resp = decorated_view(correct_token_request)

        with self.assertRaises(PermissionDenied):
            decorated_view(incorrect_token_request)

    def test_validate_pool_token(self):
        decorated_view = decorators.validate_pool_token(self.view)
        correct_token_request = self.request_factory.get(
            '/', {'token': self.pool_token.token}
        )
        incorrect_token_request = self.request_factory.get(
            '/', {'token': self.incorrect_uuid_token}
        )

        # Assert not raises
        resp = decorated_view(correct_token_request)

        with self.assertRaises(PermissionDenied):
            decorated_view(incorrect_token_request)


class AnswerProcessingTestCase(TestCase):
    def setUp(self):
        self.questions = (
            models.Question.objects.create(
                name='0', content='Content', category=models.Question.OPEN
            ),
            models.Question.objects.create(
                name='1', content='Content', category=models.Question.CLOSED
            )
        )
        self.option = models.AnswerOption.objects.create(
            question=self.questions[1], text='Opt0'
        )
        self.pool = models.Pool.objects.create(
            name='Test'
        )
        self.pool.questions.set(self.questions)
        self.pool_answer = models.PoolAnswer.objects.create(
            pool=self.pool,
            pool_token=models.PoolToken.objects.create(pool=self.pool),
            ip='127.0.0.1'
        )
    
    def test_save_answers(self):
        post_data = {
            f'question_{self.questions[0].id}': 'answer',
            f'question_{self.questions[1].id}': self.option.id,
        }
        save_answers(post_data, self.pool, self.pool_answer,
                     metadata=TeamsMetadata({}))
        self.assertEqual(models.UserAnswer.objects.all().count(), 2)
        # Was 1, should be 2
        self.assertEqual(models.AnswerOption.objects.all().count(), 2)
        