from django.contrib import admin
from .models import *

admin.site.register(Student)
admin.site.register(Article)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer)


admin.site.site_title, admin.site.site_header = 'Садыев Админ', 'Садыев Админ'