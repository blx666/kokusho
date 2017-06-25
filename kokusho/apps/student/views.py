import pyexcel
from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login
from django.http import HttpResponse, HttpResponseRedirect
from kokusho.apps.student.forms import LoginForm
from django.contrib import messages
from django.core.cache import cache


def login(request):
    if request.method != 'POST':
        return render(request, 'login.html', {'form': LoginForm()})

    user = authenticate(username=request.POST.get('number'), password=request.POST.get('password'))
    if user:
        data = cache.get('user | %s' % user.id)
        if data:
            return render(request, 'result.html', {'score_url': data, 'username': user.username})

        data = []
        auth_login(request, user)
        score_list = user.score_set.all()
        cache.set('user | %s' % user.id, data, 5*60)
        if score_list:
            for score in score_list:
                if score.exam_time.year == datetime.now().year:
                    data.append(score)

        cache.set('user | %s' % user.id, data)
        return render(request, 'result.html', {'score_url': data, 'username': user.username})

    return render(request, 'login.html', {'form': LoginForm(), 'errors': 'user or password is wrong'})


def add_student_info(request):
    if request.method != 'POST':
        return HttpResponse('request method is error')
    if not request.FILES:
        return HttpResponse('file is not null')
    student_sheet = pyexcel.get_sheet(file_type="xlsx", file_stream=request.FILES['excel_file'])
    student_infos = student_sheet.csv.split()
    student_infos.pop(0)
    invalid_student = []
    for info in student_infos:
        info_list = info.split(',')
        try:
            User.objects.create_user(username=info_list[0], password=info_list[1])
        except User.DoesNotExist:
            invalid_student.append(info)
            # return HttpResponse(info_list[0] + 'exist, has benn Stop entry')
    if invalid_student:
        messages.error(str(invalid_student) + 'exist, entry fail')
    return HttpResponseRedirect('/admin/auth/')








import os
import re
import shutil
from ftplib import FTP
from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import User
from kokusho.apps.student.models import Score
from kokusho.apps.student.utils import create_file_name

from django.core.mail import send_mail


def get_student_score(request):
    try:
        ftp = FTP()
        ftp.set_debuglevel(2)
        ftp.connect(settings.HOST, 21)
        ftp.login(settings.USERNAME, settings.PASSWORD)
    except:
        subject = 'error forms'
        message = 'ftp connect is fail'
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [settings.HOST_ADMIN], connection=None,
                  html_message=None)
    bufsize = 2048
    ftp_dir_list = ftp.nlst()
    for dir in ftp_dir_list:
        invalid_student = []
        valid_student = []
        server_dir = settings.MEDIA_ROOT + dir
        if not os.path.exists(server_dir):
            os.mkdir(server_dir)

        exam_time = datetime(int(dir[:4]), int(dir[4:]), 1)
        number_list = Score.objects.filter(exam_time=exam_time).values_list('user__username', flat=True)

        file_list = ftp.nlst(dir)
        new_file_list = []
        for file in file_list:
            number_name = re.split('[/.]', file)[-2]
            if number_name not in number_list:
                new_file_list.append(file)

        if new_file_list:

            for file in new_file_list:
                write_img = open(settings.MEDIA_ROOT + file, 'wb')
                ftp.retrbinary('RETR ' + file, write_img.write, bufsize)
                write_img.close()

                filename = re.split('[/.]', file)[-2]
                new_name = file.replace(filename, create_file_name(filename))
                os.rename(settings.MEDIA_ROOT + file, settings.MEDIA_ROOT + new_name)

                user = User.objects.filter(username=filename)
                if user:
                    valid_student.append([new_name, exam_time, user.first()])
                else:
                    invalid_student.append(filename)

            if invalid_student:
                shutil.rmtree(server_dir)
                subject = 'error forms'
                message = '%s year %s month student mark, %s student number is invalid, entry score is fail' \
                          % (dir[:4], dir[4:], invalid_student)
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [settings.HOST_ADMIN], connection=None,
                          html_message=None)
            else:
                for student in valid_student:
                    Score.objects.create(image=student[0], exam_time=student[1], user=student[2])

    ftp.close()
    return HttpResponse('success')
