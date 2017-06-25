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
    invalid_student = []
    valid_student = []
    for dir in ftp_dir_list:
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


if __name__ == "__main__":
    get_student_score()
    pass










#
#     if remote_path in ftp.nlst() and ftp.nlst(remote_path):
#         for file_path in ftp.nlst(remote_path):
#             fp = open(local_path + file_path, 'wb')
#             ftp.retrbinary('RETR ' + file_path, fp.write, bufsize)
#             ftp.set_debuglevel(0)
#             data = write_pic_server(stu_id, file_path)
#             if data:
#                 result = data
#         fp.close()
#
#     pass
#
#
# student = Student.objects.get_or_create(number=stu_id)
#     score = Score.objects.create(path=file_path, user=student[0])
#
#     filename = re.split('[/.]', file_path)[-2]
#     if stu_id == filename:
#         result.append(score.path)
#     return result


# token = user.email + str(timezone.now())
#         md5token = hashlib.md5()
#         md5token.update(token.encode('utf-8'))
#         token = md5token.hexdigest()