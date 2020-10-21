from django.db import models
from django.contrib.auth.models import User as DjangoUser


class User(DjangoUser):
    pass


class NameMixin:
    def __str__(self):
        return f'{self.name} (id: {self.id})'


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
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=False)
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
