from django.contrib import admin
import nested_admin
import core.models as models


class AnswerOptionInline(nested_admin.NestedStackedInline):
    model = models.AnswerOption


class QuestionAdmin(nested_admin.NestedModelAdmin):
    model = models.Question
    inlines = [AnswerOptionInline]


admin.site.register(models.User)
admin.site.register(models.Question, QuestionAdmin)

# For development
admin.site.register(models.AnswerOption)
admin.site.register(models.UserAnswer)
admin.site.register(models.Pool)
