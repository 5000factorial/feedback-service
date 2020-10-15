from django.contrib import admin
import core.models as models

# Register your models here.
admin.site.register(models.User)
admin.site.register(models.Question)
admin.site.register(models.AnswerOption)
admin.site.register(models.Answer)
admin.site.register(models.Pool)
