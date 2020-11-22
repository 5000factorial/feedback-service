from django.contrib import admin
import nested_admin
import core.models as models
from django.utils.html import format_html


class AnswerOptionInline(nested_admin.NestedStackedInline):
    model = models.AnswerOption


class QuestionAdmin(nested_admin.NestedModelAdmin):
    model = models.Question
    inlines = [AnswerOptionInline]


class TeamsTokenAdmin(admin.ModelAdmin):
    readonly_fields=('token',)


class PoolTokenAdminMixin:
    readonly_fields=('token', 'pool_link')
    model = models.PoolToken

    def get_queryset(self, request):
        self.request = request      
        return super().get_queryset(request)

    def pool_link(self, obj):
        url = self.request.build_absolute_uri(
            f'/pool/{obj.pool.id}/?token={obj}'
        )
        return format_html(f'<a href={url}>{url}</a>')


class PoolTokenAdmin(PoolTokenAdminMixin, admin.ModelAdmin):
    pass


class NestedPoolTokenAdmin(PoolTokenAdminMixin, nested_admin.NestedStackedInline):
    pass


class PoolAdmin(nested_admin.NestedModelAdmin):
    model = models.Pool
    inlines = [NestedPoolTokenAdmin]


admin.site.register(models.PoolUser)
admin.site.register(models.PoolToken, PoolTokenAdmin)
admin.site.register(models.TeamsToken, TeamsTokenAdmin)
admin.site.register(models.Question, QuestionAdmin)

admin.site.register(models.TeamsChannel)
admin.site.register(models.TeamsTeam)
admin.site.register(models.TeamsUser)

# For development
admin.site.register(models.AnswerOption)
admin.site.register(models.UserAnswer)
admin.site.register(models.Pool, PoolAdmin)
