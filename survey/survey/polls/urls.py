from django.urls import path
from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:survey_id>/', views.detail, name='detail'),
    path('<int:survey_id>/edit/', views.edit, name='edit'),
]