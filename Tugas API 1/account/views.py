import sys
import uuid
from django.contrib import messages
from django.db.models.signals import post_save
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.db.models import Q
from django.contrib.auth.models import User
from account.models import AccountUser, Course, AttendingCourse
from account.signals import check_nim
from account.forms import StudentRegisterForm, CourseForm
from django.http import HttpResponse


def home(request):
    return render(request, 'home.html')

def readCourse(request):
    data = Course.objects.all()[:1]
    context = {'data_list': data}
    return render(request, 'course.html', context)

# def createCourse(request):
#     if request.method == 'POST':
#         form = CourseForm(request.POST)
#         if form.is_valid():
#             course = form.save(commit=False)
#             course.course_created_by = request.user.username
#             course.save()
#             return redirect('read-data-course')
#     else:
#         form = CourseForm()
#     return render(request, 'course_form.html', {'form': form})
#
# def updateCourse(request, course_id):
#     course = Course.objects.get(course_id=course_id)
#     if request.method == 'POST':
#         form = CourseForm(request.POST, instance=course)
#         if form.is_valid():
#             course = form.save(commit=False)
#             course.course_updated_by = request.user.username
#             course.save()
#             return redirect('read-data-course', course_id=course.course_id)
#     else:
#         form = CourseForm(instance=course)
#     return render(request, 'course_form.html', {'form': form})
def createCourse(request):
    return render(request, 'course.html', {})

def updateCourse(request):
    return render(request, 'course.html')


def deleteCourse(request, id):
    try:
        data = Course.objects.filter(course_id=id)
        if user:
            data.delete()
            messages.success(request, 'Data Berhasil dihapus')
            return redirect('account:read-data-course')
        else:
            messages.success(request, 'Data Tidak ditemukan')
            return redirect('account:read-data-course')
    except:
        return redirect('account:read-data-course')


def readStudent(request):

    data = AccountUser.objects.all()

    context = {'data_list': data}

    return render(request, 'index.html', context)



@csrf_protect
def createStudent(request):
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            fullname = form.cleaned_data.get("fullname")
            nim = form.cleaned_data.get("nim")
            email = form.cleaned_data.get("email")

            user, created = User.objects.get_or_create(username=email)
            if created:
                user.save()

            account_user = AccountUser(account_user_related_user=user, account_user_fullname=fullname, account_user_student_number=nim)
            account_user.save()

            messages.success(request, 'Data Berhasil disimpan')
            return redirect('account:read-data-student')
    else:
        form = StudentRegisterForm()
    return render(request, 'form.html', {'form': form})



@csrf_protect
def updateStudent(request, id):
    member = AccountUser.objects.get(account_user_related_user=id)
    user = User.objects.get(username=id)
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            account_user_student_number = form.cleaned_data.get("nim")
            email = form.cleaned_data.get("email")

            if account_user_student_number:
                member.account_user_student_number = account_user_student_number
            else:
                messages.error(request, 'Account user student number is required')
                return render(request, 'update_student.html', {'form': form})

            user.email = email
            member.save()
            user.save()
            messages.success(request, 'Data Berhasil diupdate')
            return redirect('account:read-data-student')
        else:
            print(form.errors)
    else:
        initial_data = {
            'fullname': user.first_name + '' + user.last_name,
            'nim': member.account_user_student_number,
            'email': user.email,
        }
        form = StudentRegisterForm(initial=initial_data)
    return render(request, 'update_student.html', {'form': form})


@csrf_protect
def deleteStudent(request, id):
    member = AccountUser.objects.get(account_user_related_user=id)
    user = User.objects.get(username=id)
    if request.method == 'POST':
        member.delete()
        user.delete()
        messages.success(request, 'Data Berhasil dihapus')
        return redirect('account:read-data-student')
    return render(request, 'delete_confirm.html', {'object': member})
