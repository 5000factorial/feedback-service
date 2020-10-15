from django.db import models
from django.contrib.auth.models import User as DjangoUser


class User(DjangoUser):
    pass


class Question(models.Model):
    content = models.JSONField(null=False)


class AnswerOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=False)
    text = models.JSONField(null=False)


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=False)
    option = models.ForeignKey(AnswerOption, on_delete=models.CASCADE, null=False)


class Pool(models.Model):
    questions = models.ManyToManyField(Question)
