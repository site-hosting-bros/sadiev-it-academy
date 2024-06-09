from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Article, Student, Quiz, Question, Answer
from .forms import UserForm, StudentForm

def home(request):
    articles = Article.objects.all()
    return render(request, 'main/home.html', {'articles': articles})

def article_list(request):
    articles = Article.objects.all()
    return render(request, 'main/article_list.html', {'articles': articles})

def article_detail(request, id):
    article = get_object_or_404(Article, id=id)
    link = "https://www.youtube.com/embed/" + str(article.video)
    print("ССЫЛОЧКА: ",link)
    return render(request, 'main/article_detail.html', {'article': article, 'link' : link})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'main/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'main/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def profile(request):
    user = request.user
    try:
        student = user.student
    except Student.DoesNotExist:
        student = Student(user=user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        student_form = StudentForm(request.POST, instance=student)
        if user_form.is_valid() and student_form.is_valid():
            user_form.save()
            student_form.save()
            return redirect('profile')
    else:
        user_form = UserForm(instance=user)
        student_form = StudentForm(instance=student)

    context = {
        'user_form': user_form,
        'student_form': student_form
    }
    return render(request, 'main/profile.html', context)

def about(request):
    return render(request, 'main/about.html')

def quiz(request):
    return render(request, 'main/quiz.html')

def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'main/quiz_list.html', {'quizzes': quizzes})

def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.question_set.all()
    if request.method == 'POST':
        correct_answers = 0
        for question in questions:
            selected_answer_id = request.POST.get(f'question_{question.id}')
            if selected_answer_id:
                selected_answer = get_object_or_404(Answer, id=selected_answer_id)
                if selected_answer.is_correct:
                    correct_answers += 1
        score = (correct_answers / questions.count()) * 100
        return render(request, 'main/quiz_result.html', {'quiz': quiz, 'score': score})
    return render(request, 'main/quiz_detail.html', {'quiz': quiz, 'questions': questions})