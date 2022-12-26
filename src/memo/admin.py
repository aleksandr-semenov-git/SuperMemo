from django.contrib import admin

from lesson.models import Section, Theme, Lesson, Question
from .models import *

admin.site.register(Profile)
admin.site.register(Goal)
admin.site.register(Section)
admin.site.register(Theme)
admin.site.register(Question)
admin.site.register(Lesson)
