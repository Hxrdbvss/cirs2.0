from django.contrib import admin
from .models import Survey, Question, Choice, Answer

@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'question_count')
    search_fields = ('title',)

    def question_count(self, obj):
        return obj.questions.count()
    question_count.short_description = 'Кол-во вопросов'

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'survey', 'question_type')
    list_filter = ('survey', 'question_type')
    search_fields = ('question_text',)

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'votes')
    list_filter = ('question',)
    search_fields = ('text',)

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'choice', 'text_answer', 'created_at')
    list_filter = ('question', 'created_at')
    search_fields = ('text_answer',)
