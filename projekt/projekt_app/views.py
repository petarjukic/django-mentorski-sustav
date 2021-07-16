from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseNotAllowed
from django.db.models import Count
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from .models import Korisnik, Predmet, Upisi
from .forms import *
from .decoratos import mentor_required
from django.contrib import messages

# Create your views here.


@login_required
def home_page(request):
    return render(request, 'home.html', {})


def logout_view(request): 
    logout(request)
    return render(request, 'logout.html', {})


def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'GET':
        userForm = RegistrationForm()
        return render(request, 'register.html', {'form':userForm})
    elif request.method == 'POST':
        userForm = RegistrationForm(request.POST)
        if userForm.is_valid():
            user = userForm.save()
            return redirect('login')
        else:
            return render(request, 'register.html', {'form':userForm})
    else:
        return HttpResponseNotAllowed


@login_required
@user_passes_test(lambda u: u.role=='MENTOR')
def all_students(request):
    studenti = Korisnik.objects.all()
    return render(request, 'all_students.html', {'studenti':studenti})


@login_required
@user_passes_test(lambda u: u.role=='MENTOR')
def courses(request):
    predmeti = Predmet.objects.all()
    return render(request, 'courses.html', {'predmeti':predmeti})


@login_required
@user_passes_test(lambda u: u.role=='MENTOR')
def insert_course(request):
    predmet = Predmet.objects.all()
    
    if request.method == 'GET':
        course_form = PredmetForm()
        return render(request, 'insert_course.html', {'form':course_form})
    elif request.method == 'POST':
        course_form = PredmetForm(request.POST)
        if Predmet.objects.filter(ime=request.POST['ime']) or Predmet.objects.filter(kod=request.POST['kod']):
            messages.info(request, 'Nije moguce unijeti predmet jer je ime i/ili kod postojeci!!')
            return redirect('home')
        if course_form.is_valid():
            course_form.save()
            return redirect('courses')
        else:
            return HttpResponseNotAllowed()


@login_required
@user_passes_test(lambda u: u.role=='MENTOR')
def edit_course(request, course_id):
    course = Predmet.objects.get(id=course_id)

    if request.method == 'GET':
        set_form = PredmetForm(instance=course)
        return render(request, 'edit_course.html', {'form':set_form})
    elif request.method == 'POST':
        set_form = PredmetForm(request.POST, instance=course)
        if set_form.is_valid():
            set_form.save()
            return redirect('courses')


@login_required
@user_passes_test(lambda u: u.role=='MENTOR')
def course_detail(request, course_id):
    course = Predmet.objects.filter(id=course_id)
    return render(request, 'detail_course.html', {'course':course})


@login_required
def upisni_list(request, student_id):
    predmeti = Predmet.objects.all()
    student = Korisnik.objects.get(id=student_id)
    upisani = Upisi.objects.filter(student_id=student.id)
    predmet_id = Upisi.objects.filter(student_id=student.id).values_list('predmet_id', flat=True)
    neupisani = {}
    
    for i in predmeti:
        if i.id not in predmet_id:
            neupisani[i.id] = i.ime

    context = {
        'predmeti':predmeti,
        'ime':student,
        'upisani':upisani,
        'neupisani':neupisani
    }
    return render(request, 'upisni_list.html', context)


def ispis_predmeta(request, predmet_id, student_id):
    predmet = Upisi.objects.filter(predmet_id=predmet_id, student_id=student_id)
    predmet.delete()
    return redirect('upisni_list', student_id)


def upis_predmeta(request, predmet_id, student_id):
    predmet = Predmet.objects.get(id=predmet_id)
    student = Korisnik.objects.get(id=student_id)
    Upisi.objects.create(predmet_id=predmet, student_id=student, status='nepolozen')
    return redirect('upisni_list', student_id)
    

def polozio_predmet(request, predmet_id, student_id):
    promjena = Upisi.objects.filter(predmet_id=predmet_id, student_id=student_id).update(status='polozen')
    return redirect('upisni_list', student_id)
    

def delete_course(request, course_id):
    predmet = Predmet.objects.get(id=course_id)
    predmet.delete()
    return redirect('courses')
