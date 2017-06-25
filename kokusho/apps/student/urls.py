from django.conf.urls import url
from kokusho.apps.student.views import login, add_student_info, get_student_score
import django
from kokusho import settings

urlpatterns = [
    url(r'^/$', login, name='login'),
    url(r'^login/$', login, name='login'),
    url(r'^admin/auth/add-student-info/$', add_student_info, name='add-student-info'),
    url(r'^test/$', get_student_score, name='get-student-score'),
    url(r'^media/student/*/(?P<path>.*)/$', django.views.static.serve, {'document_root': settings.MEDIA_ROOT}),
    # url(r'^media/(?P<path>.*)/$', django.views.static.serve, {'document_root': settings.MEDIA_ROOT}),
]
