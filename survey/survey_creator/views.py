from django.shortcuts import render, get_object_or_404, redirect
from django.forms import formset_factory
from polls.models import Survey, Question, Choice, Answer
from .forms import SurveyForm, QuestionFormSet, ChoiceFormSet

def create_survey(request):
    if request.method == 'POST':
        print("POST data:", request.POST)  # Отладка
        # Создаём опрос
        title = request.POST.get('title')
        if not title:
            return render(request, 'survey_creator/create_survey.html', {'error': 'Введите название опроса'})
        survey = Survey.objects.create(title=title)

        # Обрабатываем вопросы
        question_index = 0
        while f'question-{question_index}-text' in request.POST:
            question_text = request.POST.get(f'question-{question_index}-text')
            question_type = request.POST.get(f'question-{question_index}-type')
            if question_text and question_type:
                question = Question.objects.create(
                    survey=survey,
                    text=question_text,
                    question_type=question_type
                )
                # Обрабатываем варианты ответа
                if question_type != 'text':
                    choice_index = 0
                    while f'choice-{question_index}-{choice_index}-text' in request.POST:
                        choice_text = request.POST.get(f'choice-{question_index}-{choice_index}-text')
                        if choice_text:
                            Choice.objects.create(question=question, text=choice_text)
                        choice_index += 1
            question_index += 1
        
        return redirect('polls:index')
    
    return render(request, 'survey_creator/create_survey.html')

def add_questions(request, survey_id):
    survey = get_object_or_404(Survey, pk=survey_id)
    if request.method == 'POST':
        question_formset = QuestionFormSet(request.POST, prefix='questions')
        
        if question_formset.is_valid():
            for question_form in question_formset:
                if question_form.cleaned_data:
                    question = question_form.save(commit=False)
                    question.survey = survey
                    question.save()
                    
                    if question.question_type != 'text':
                        choice_formset = ChoiceFormSet(request.POST, prefix=f'choices-{question_form.prefix}')
                        if choice_formset.is_valid():
                            for choice_form in choice_formset:
                                if choice_form.cleaned_data:
                                    choice = choice_form.save(commit=False)
                                    choice.question = question
                                    choice.save()
            return redirect('polls:index')
    else:
        question_formset = QuestionFormSet(prefix='questions')
    
    choice_formsets = [ChoiceFormSet(prefix=f'choices-questions-{i}') for i in range(question_formset.total_form_count())]
    
    return render(request, 'survey_creator/add_questions.html', {
        'survey': survey,
        'question_formset': question_formset,
        'choice_formsets': choice_formsets,
    })