import sys
from django.contrib import messages
from django.db.models.signals import post_save
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.db.models import Q
from django.contrib.auth.models import User
from account.models import AccountUser
from account.signals import check_nim
from account.forms import StudentRegisterForm


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

            account_user, created = AccountUser.objects.get_or_create(account_user_related_user=email)
            if created:
                account_user.account_user_fullname = fullname
                account_user.account_user_student_number = nim
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
