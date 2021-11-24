import factory.fuzzy
from memo import models


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.User
    username = factory.Sequence(lambda n: f'test_user{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.test')


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Profile

    user = factory.SubFactory(UserFactory)


class GoalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Goal

    name = factory.Sequence(lambda n: 'goal%d' % n)
    profile = factory.SubFactory(ProfileFactory)


class SectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Section

    name = factory.Sequence(lambda n: 'section%d' % n)
    goal = factory.SubFactory(GoalFactory)


class ThemeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Theme

    name = factory.Sequence(lambda n: 'theme%d' % n)
    section = factory.SubFactory(SectionFactory)


class LessonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Lesson

    name = factory.Sequence(lambda n: '%d' % n)
    profile = factory.SubFactory(ProfileFactory)
    goal = factory.SubFactory(GoalFactory)


class QuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Question

    question = factory.Sequence(lambda n: 'question%d' % n)
    answer = factory.Sequence(lambda n: 'answer%d' % n)
    goal = factory.SubFactory(GoalFactory)
    lesson = factory.SubFactory(LessonFactory)
    section = factory.SubFactory(SectionFactory)
    theme = factory.SubFactory(ThemeFactory)
