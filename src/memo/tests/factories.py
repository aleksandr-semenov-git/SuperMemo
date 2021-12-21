import factory.fuzzy

import account.models
import lesson.models
from memo import models
from django.contrib.auth.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    username = 'test_user0'
    email = 'test@test.email'
    # email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.test')


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = account.models.Profile

    user = factory.SubFactory(UserFactory)


class GoalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Goal

    # name = 'test_goal_name'
    name = factory.Sequence(lambda n: 'goal%d' % n)
    profile = factory.SubFactory(ProfileFactory)


class SectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = lesson.models.Section

    name = 'test_section_name'
    # name = factory.Sequence(lambda n: 'section%d' % n)
    goal = factory.SubFactory(GoalFactory)


class ThemeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = lesson.models.Theme

    name = 'test_theme_name'
    # name = factory.Sequence(lambda n: 'theme%d' % n)
    section = factory.SubFactory(SectionFactory)


class LessonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = lesson.models.Lesson

    name = factory.Sequence(lambda n: '%d' % n)
    profile = factory.SubFactory(ProfileFactory)
    goal = factory.SubFactory(GoalFactory)


class QuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = lesson.models.Question

    question = factory.Sequence(lambda n: 'question%d' % n)
    answer = factory.Sequence(lambda n: 'answer%d' % n)
    goal = factory.SubFactory(GoalFactory)
    lesson = factory.SubFactory(LessonFactory)
    section = factory.SubFactory(SectionFactory)
    theme = factory.SubFactory(ThemeFactory)
