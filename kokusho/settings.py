from kokusho.django_settings import *

USERNAME = 'bilixin'
PASSWORD = '123456'
HOST = '127.0.1'

HOST_ADMIN = 'admin@qq.com'

# email
# https://docs.djangoproject.com/en/1.10/topics/email/
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25

DEFAULT_FROM_EMAIL = "donotreply@itscoastal.com"

# cron
CRONJOBS = [
    ('00 00 * * *', 'kokusho.apps.student.cronjobs.get_student_score'),
]