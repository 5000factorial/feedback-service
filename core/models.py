from django.db import models
from django.contrib.auth.models import User as DjangoUser
from datetime import timedelta
import uuid


class NameMixin:
    def __str__(self):
        return f'{self.name} (id: {self.id})'


class TeamsToken(models.Model):
    token = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, verbose_name='Токен')

    def __str__(self):
        return str(self.token)

    class Meta:
        verbose_name = 'Токен MS Teams'
        verbose_name_plural = 'Токены MS Teams'


class Question(NameMixin, models.Model):
    OPEN = 'open'
    CLOSED = 'closed'
    CATEGORIES = [
        (OPEN, 'Open (Free answer)'),
        (CLOSED, 'Closed (Fixed answer options)')
    ]

    content = models.TextField(null=False, verbose_name='Текст')
    name = models.CharField(max_length=128, null=False, verbose_name='Название')
    category = models.CharField(
        max_length=16,
        choices=CATEGORIES,
        default=CLOSED,
        verbose_name = 'Категория'
    )

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class AnswerOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=False, related_name='options', verbose_name='Вопрос')
    text = models.TextField(null=False, help_text='Text representation of answer option', verbose_name='Текст')

    def __str__(self):
        return f'{self.text[0:32]} (id: {self.id}, q: {self.question.name})'

    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответа'


class Pool(NameMixin, models.Model):
    name = models.CharField(max_length=256, null=False, verbose_name='Название')
    questions = models.ManyToManyField(Question, verbose_name='Вопросы')

    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'


class PoolToken(models.Model):
    token = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, verbose_name='Токен')
    pool = models.ForeignKey(Pool, on_delete=models.CASCADE, null=False, verbose_name='Опрос')
    
    one_time = models.BooleanField(default=False, verbose_name='Одноразовый')

    # allow_after = models.DurationField(default=timedelta(seconds=0))

    def __str__(self):
        return f'{str(self.pool)} - {str(self.token)}'

    class Meta:
        verbose_name = 'Токен опроса'
        verbose_name_plural = 'Токены опроса'


class TeamsTeam(models.Model):
    uid = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=256, verbose_name='Название')

    def __str__(self):
        return f'{self.name} (id: {str(self.uid)[:8]}...)'

    class Meta:
        verbose_name = 'Команда MS Teams'
        verbose_name_plural = 'Команды MS Teams'



class TeamsChannel(models.Model):
    uid = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=256, verbose_name='Название')
    team = models.ForeignKey(TeamsTeam, on_delete=models.CASCADE, null=False, verbose_name='Команда MS Teams')

    def __str__(self):
        return f'{self.name} - {self.team.name} (id: {str(self.uid)[:8]}...)'

    class Meta:
        verbose_name = 'Канал MS Teams'
        verbose_name_plural = 'Каналы MS Teams'


class TeamsUser(models.Model):
    uid = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=256, verbose_name='Название')

    def __str__(self):
        return f'{self.name} (id: {str(self.uid)[:8]}...)'

    class Meta:
        verbose_name = 'Пользователь MS Teams'
        verbose_name_plural = 'Пользователи MS Teams'


class PoolAnswer(models.Model):
    pool = models.ForeignKey(Pool, on_delete=models.CASCADE, null=False, verbose_name='Опрос')
    pool_token = models.ForeignKey(PoolToken, on_delete=models.CASCADE, null=False, verbose_name='Токен опроса')
    ip = models.GenericIPAddressField()
    teams_channel = models.ForeignKey(TeamsChannel, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Канал MS Teams')
    teams_user = models.ForeignKey(TeamsUser, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Пользователь MS Teams')

    class Meta:
        verbose_name = 'Результат опроса'
        verbose_name_plural = 'Результаты опроса'


class UserAnswer(models.Model):
    user = models.ForeignKey(TeamsUser, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Пользователь MS Teams')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=False, verbose_name='Вопрос')
    option = models.ForeignKey(AnswerOption, on_delete=models.CASCADE, null=False, verbose_name='Вариант ответа')
    pool_answer = models.ForeignKey(PoolAnswer, on_delete=models.CASCADE, verbose_name='Результат опроса')

    class Meta:
        verbose_name = 'Ответ на вопрос'
        verbose_name_plural = 'Ответы на вопрос'
