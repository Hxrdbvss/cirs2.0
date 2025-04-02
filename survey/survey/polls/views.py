from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import Survey, Question, Choice, Answer

def index(request):
    surveys = Survey.objects.all()
    if request.method == 'POST' and 'delete_survey' in request.POST:
        survey_id = request.POST.get('survey_id')
        survey = get_object_or_404(Survey, pk=survey_id)
        survey.delete()
        return redirect('polls:index')
    return render(request, 'polls/index.html', {'surveys': surveys})

def detail(request, survey_id):
    survey = get_object_or_404(Survey, pk=survey_id)
    context = {'survey': survey}
    
    if request.method == 'POST':
        print("POST data:", request.POST)
        questions = survey.questions.all()
        for question in questions:
            if question.question_type == 'radio':
                choice_id = request.POST.get(f'question_{question.id}')
                if choice_id:
                    choice = get_object_or_404(Choice, pk=choice_id, question=question)
                    Answer.objects.create(question=question, choice=choice)
                else:
                    context['error_message'] = f'Выберите вариант для вопроса "{question.text}"'
                    return render(request, 'polls/detail.html', context)
            elif question.question_type == 'checkbox':
                choice_ids = request.POST.getlist(f'question_{question.id}')
                if choice_ids:
                    for choice_id in choice_ids:
                        choice = get_object_or_404(Choice, pk=choice_id, question=question)
                        Answer.objects.create(question=question, choice=choice)
                else:
                    context['error_message'] = f'Выберите хотя бы один вариант для вопроса "{question.text}"'
                    return render(request, 'polls/detail.html', context)
            elif question.question_type == 'text':
                text_answer = request.POST.get(f'question_{question.id}')
                if text_answer and text_answer.strip():
                    Answer.objects.create(question=question, text_answer=text_answer)
                else:
                    context['error_message'] = f'Введите текст для вопроса "{question.text}"'
                    return render(request, 'polls/detail.html', context)
        
        context['show_thanks'] = True
        return render(request, 'polls/detail.html', context)
    
    return render(request, 'polls/detail.html', context)

def edit(request, survey_id):
    survey = get_object_or_404(Survey, pk=survey_id)
    if request.method == 'POST':
        if 'delete_survey' in request.POST:
            survey.delete()
            return redirect('polls:index')

        # Обновляем название опроса
        survey.title = request.POST.get('survey_title', survey.title)
        survey.save()

        # Удаляем старые вопросы и варианты, если они не в POST
        existing_questions = {str(q.id): q for q in survey.questions.all()}
        new_questions = {}

        # Обрабатываем вопросы
        for key in request.POST:
            if key.startswith('question_text_'):
                q_id = key.split('_')[-1]
                if q_id in existing_questions:
                    question = existing_questions[q_id]
                else:
                    question = Question(survey=survey)
                
                question.text = request.POST.get(f'question_text_{q_id}')
                question.question_type = request.POST.get(f'question_type_{q_id}')
                question.save()
                new_questions[q_id] = question

                # Обрабатываем варианты ответа
                if question.question_type in ['radio', 'checkbox']:
                    existing_choices = {str(c.id): c for c in question.choices.all()}
                    new_choices = {}
                    for choice_key in request.POST.getlist(f'choice_text_{q_id}'):
                        if choice_key and choice_key.strip():
                            choice_id = request.POST.get(f'choice_id_{q_id}_{choice_key}')
                            if choice_id and choice_id in existing_choices:
                                choice = existing_choices[choice_id]
                                choice.text = choice_key
                            else:
                                choice = Choice(question=question, text=choice_key)
                            choice.save()
                            new_choices[choice.id] = choice
                    
                    # Удаляем варианты, которых больше нет
                    for cid, choice in existing_choices.items():
                        if cid not in new_choices:
                            choice.delete()

        # Удаляем вопросы, которых больше нет
        for qid, question in existing_questions.items():
            if qid not in new_questions:
                question.delete()

        return redirect('polls:index')

    return render(request, 'polls/edit.html', {'survey': survey})