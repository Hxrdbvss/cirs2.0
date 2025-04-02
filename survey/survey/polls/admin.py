from django.contrib import admin
from .models import Survey, Question, Choice, Answer

@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ('title',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'survey', 'question_type')
    list_filter = ('survey', 'question_type')

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('text', 'question')
    list_filter = ('question',)

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'choice', 'text_answer', 'created_at')
    list_filter = ('question', 'created_at')