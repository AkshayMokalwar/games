from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate
from .forms import RegistrationForm,UserUpdateForm,UserLoginForm
from .models import UserProfile
from quiz.models import QuizSession
from django.contrib.auth.decorators import login_required
import json
from django.views.decorators.csrf import csrf_exempt

from movies.models import Movie, Clue

import random
import string

def generate_session_code(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

@login_required
def create_room(request):
    if request.method == "POST":
        mode = request.POST.get("mode", "CS")
        session_code = generate_session_code(8)

        session = QuizSession.objects.create(
            session_code=session_code,
            host=request.user.userprofile,
            mode=mode
        )
        session.participants.add(request.user.userprofile)  # host is also participant
        return redirect('quiz:room_lobby', session_code=session_code)

@login_required
def join_room(request):
    if request.method == "POST":
        code = request.POST.get("session_code").upper()
        try:
            session = QuizSession.objects.get(session_code=code, is_active=True)
            session.participants.add(request.user.userprofile)
            return redirect('quiz:room_lobby', session_code=code)
        except QuizSession.DoesNotExist:
            print(request, "Room not found or inactive.")
            return redirect('quiz:join_room_page')

# from .forms import RegistrationForm
@login_required
def room_lobby(request, session_code):
    session = get_object_or_404(QuizSession, session_code=session_code)
    participants = session.participants.all()
    return render(request, 'quiz/room_lobby.html', {
        'session': session,
        'participants': participants,
        'is_host': request.user.userprofile == session.host
    })

@csrf_exempt  # only for testing; better to use csrf token correctly
def submit_guess(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode("utf-8"))
            clue_id = data.get('clue_id')
            session_code = data.get('session_code')
            movie_exp= data.get('movie_exp')
            guess = data.get('guess')
            timestamp = data.get('timestamp')

            # Process logic here (you can validate guess, score, etc.)
            correct = guess.lower().strip() == movie_exp.lower().strip()  # dummy check

            return JsonResponse({"correct": correct})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request"}, status=405)


# def submit_guess(request):
#     data = json.loads(request.body)
#     session_code = data['session_code']
#     guess = data['guess']
#     clue_id = data['clue_id']
#     timestamp = data['timestamp']

#     session = get_object_or_404(QuizSession, session_code=session_code)
#     clue = get_object_or_404(Clue, id=clue_id)

#     correct = clue.movie.title.lower().strip() == guess.lower().strip()

#     UserAnswer.objects.create(
#         session=session,
#         clue=clue,
#         user_answer=guess,
#         is_correct=correct,
#         lifelines_used={},  # fill later if needed
#         user=request.user.userprofile
#     )

#     if correct:
#         session.score += 1
#         session.save()

#     return JsonResponse({'correct': correct})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/dashboard/')
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})

# def profile(request):
#     if request.method == 'POST':
#         userp=request.user.userprofile
#         # form = UserProfile(request.POST, request.FILES, instance=userp)
#         if userp:
#             return render(request, 'users/home.html', {'userp': userp})
#     else:
#         form = UserUpdateForm()
#     return render(request, 'users/register.html', {'form': form})

def update_profile(request):
    pass


@login_required
def dashboard(request):
    user = request.user.userprofile
    print(f"user : {user}")
    if user:
        
        # QuizSession_list = UserProfile.objects.filter(user=user.userprofile)
        # print(QuizSession_list)
        # courses = Course.objects.filter(status='active')
        # Initialize session
        
        hosted_session = QuizSession.objects.filter(
            host=user,
            is_active=True
        ).order_by('session_code')
        participated_session=[]
        participated_session = QuizSession.objects.filter(
            participants=user,
            is_active=True
        ).order_by('session_code')
        if len(hosted_session) == 0:
            session_code = generate_session_code(8)

            hosted_session = QuizSession.objects.create(
                session_code=session_code,
                host=user,
                mode='CS'
            )
          
            
        print(f"session : {hosted_session[0].session_code}")
        
        return render(request,'users/dashboard.html',{'user':user,'hosted_sessions':hosted_session,'participated_sessions':participated_session})
        # return render(request, 'version0/student_dashboard.html', {'courses_list': courses_list,'var':var,'user':user})
    else:
        msg="Invalid User Role !!! Please register again with valid role!!"
        
        return render(request, 'Failed.html',{'msg':msg})

    

def profile(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # user.role = 'student'  # Set default role
            user.save()
            login(request, user)
            return redirect('/dashboard/')  # Replace with your desired redirect
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})
    

def LoginViews(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/dashboard/')  # Replace with your desired redirect
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})
