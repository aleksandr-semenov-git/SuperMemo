from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from .serializers import LessonSerializer, SectionSerializer, ThemeSerializer
from lesson.models import Lesson, Section, Theme, Question


class Lessons(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class Sections(generics.ListAPIView):
    serializer_class = SectionSerializer
    queryset = Section.objects.all()


class SectionDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SectionSerializer
    queryset = Section.objects.all()


class Themes(generics.ListAPIView):
    serializer_class = ThemeSerializer
    queryset = Theme.objects.all()


class ThemeDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ThemeSerializer
    queryset = Theme.objects.all()


class APILessons(ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


