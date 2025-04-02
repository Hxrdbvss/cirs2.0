from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('polls/', include('polls.urls')),
    path('survey_creator/', include('survey_creator.urls')),  # Исправлено с 'creat' на 'survey_creator'
]