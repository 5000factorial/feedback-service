from django.db import models
from django.contrib.auth.models import User as DjangoUser
import uuid


class NameMixin:
    def __str__(self):
        return f'{self.name} (id: {self.id})'


class User(DjangoUser):
    pass
# class User(models.Model):
#     email = models.EmailField(null=True)


class TeamsToken(models.Model):
    token = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return str(self.token)


class Question(NameMixin, models.Model):
    OPEN = 'open'
    CLOSED = 'closed'
    CATEGORIES = [
        (OPEN, 'Open (Free answer)'),
        (CLOSED, 'Closed (Fixed answer options)')
    ]

    content = models.TextField(null=False)
    name = models.CharField(max_length=128, null=False)
    category = models.CharField(
        max_length=16,
        choices=CATEGORIES,
        default=CLOSED,
    )


class AnswerOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=False, related_name='options')
    text = models.TextField(null=False, help_text='Text representation of answer option')

    def __str__(self):
        return f'{self.text[0:32]} (id: {self.id}, q: {self.question.name})'


class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=False)
    option = models.ForeignKey(AnswerOption, on_delete=models.CASCADE, null=False)


class Pool(NameMixin, models.Model):
    name = models.CharField(max_length=256, null=False)
    questions = models.ManyToManyField(Question)


# class PoolAnswer(models.Model)

class PoolToken(models.Model):
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    pool = models.ForeignKey(Pool, on_delete=models.CASCADE, null=False)
    # one_time = models.BooleanField(default=False)

    # For external integration

    def __str__(self):
        return str(self.token)
