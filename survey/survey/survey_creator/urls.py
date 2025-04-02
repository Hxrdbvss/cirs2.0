from django.urls import path
from . import views

app_name = 'survey_creator'

urlpatterns = [
    path('create/', views.create_survey, name='create_survey'),
    path('add/<int:survey_id>/', views.add_questions, name='add_questions'),
]