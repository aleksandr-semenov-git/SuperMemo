import os
from unittest.mock import patch, MagicMock
from django.http import HttpResponse, HttpResponseRedirect
from django.test import TestCase, RequestFactory, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import authenticate, login
import factory

from lesson.views import SurePage, LessonPage, EndLessonPage
from memo.views import ProfilePage, ProfilePageBasic, EditPage, HomePage, GoalPage
from memo.forms import PersonalDataEditForm, AddGoalForm
from memo.models import Profile, Goal, Section, Theme, Question, Lesson
from memo.tests.factories import UserFactory, ProfileFactory, GoalFactory, SectionFactory, ThemeFactory, LessonFactory,\
    QuestionFactory
os.environ['DJANGO_SETTINGS_MODULE'] = 'src.settings'


class LessonTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.user = UserFactory()
        self.user.set_password('121212test')
        self.user.save()
        self.profile = ProfileFactory(user=self.user)
        self.goal = GoalFactory(profile=self.profile)
        self.section1 = SectionFactory.create(goal=self.goal)
        self.section2 = SectionFactory.create(goal=self.goal)
        self.theme1 = ThemeFactory.create(section=self.section1, goal=self.goal)
        self.theme2 = ThemeFactory.create(section=self.section1, goal=self.goal)

        self.lesson1 = LessonFactory.create(profile=self.profile,
                                            goal=self.goal)
        self.lesson2 = LessonFactory.create(profile=self.profile,
                                            goal=self.goal)

    def test_user_get_sure_page_v1(self):
        expected_result = HttpResponse
        login = self.client.login(username='test_user3', password='121212test')
        # Todo Подумать над использованием factoryboy, в каком порядке создаются юзеры?
        section = Section.objects.get(pk=1)
        theme = Theme.objects.get(pk=1)
        goal = Goal.objects.get(pk=1)
        session = self.client.session
        session['lesson_section_id'] = 1
        session['lesson_theme_id'] = 1
        session['goal_id'] = 1
        session.save()
        actual_result = self.client.get(reverse('lesson:sure'))

        self.assertEqual(actual_result.context['section'], section)
        self.assertEqual(actual_result.context['theme'], theme)
        self.assertEqual(actual_result.context['goal'], goal)
        self.assertTemplateUsed(actual_result, 'sure_page.html')

    @patch('lesson.views.lesson.render')
    @patch('lesson.views.lesson.Section.objects')
    @patch('lesson.views.lesson.Theme.objects')
    @patch('lesson.views.lesson.Goal.objects')
    def test_user_get_sure_page_v2(self, mock_goal_model, mock_theme_model, mock_section_model, mock_render):
        mock_goal = MagicMock()
        mock_section = MagicMock()
        mock_theme = MagicMock()
        mock_goal_model.get.return_value = mock_goal
        mock_section_model.get.return_value = mock_section
        mock_theme_model.get.return_value = mock_theme

        factory = RequestFactory()
        request = factory.get('new_lesson/confirm/')
        session = self.client.session
        request.session = session
        request.user = MagicMock()
        session['lesson_section_id'] = 1
        session['lesson_theme_id'] = 1
        session['goal_id'] = 1
        session.save()
        actual_result = SurePage.as_view()(request)
        mock_render.assert_called_once_with(request,
                                            'sure_page.html',
                                            {'goal': mock_goal, 'section': mock_section, 'theme': mock_theme})

    @patch('lesson.views.lesson.redirect')
    def test_user_post_sure_page(self, mock_redirect):
        expected_result = HttpResponseRedirect(redirect_to='learning-page/lesson/')
        login = self.client.login(username='test_user9', password='121212test')
        # Todo Подумать над использованием factoryboy, в каком порядке создаются юзеры?
        mock_redirect.return_value = expected_result
        actual_result = self.client.post(reverse('lesson:sure'))
        mock_redirect.assert_called_once_with('lesson:lesson_page')
        self.assertEqual(expected_result, actual_result)

    @patch('lesson.views.lesson.render')
    @patch('lesson.views.lesson.Goal.objects')
    @patch('lesson.views.lesson.Lesson.objects')
    @patch('lesson.views.lesson.LearningForm')
    def test_user_get_lesson_page_inactive_lesson(self, mock_form, mock_lesson_model, mock_goal_model, mock_render):
        expected_result = HttpResponse()
        factory = RequestFactory()
        request = factory.get('learning-page/lesson/')
        mock_profile = MagicMock()
        mock_goal = MagicMock()
        mock_lesson = MagicMock()
        form = MagicMock()
        request.user = MagicMock()
        request.user.profile = mock_profile

        session = self.client.session
        request.session = session
        session['goal_id'] = 1
        session.save()

        mock_render.return_value = expected_result
        mock_goal_model.get.return_value = mock_goal
        mock_name = mock_goal.lessons.count.return_value = 2
        mock_lesson_model.create.return_value = mock_lesson
        mock_form.return_value = form

        actual_result = LessonPage.as_view()(request)
        mock_lesson_model.create.assert_called_once_with(name=3, goal=mock_goal, profile=mock_profile)
        mock_render.assert_called_once_with(request, 'lesson.html', {'form': form, 'lesson': mock_lesson})
        self.assertEqual(expected_result, actual_result)

    @patch('lesson.views.lesson.render')
    @patch('lesson.views.lesson.Goal.objects')
    @patch('lesson.views.lesson.Lesson.objects')
    @patch('lesson.views.lesson.LearningForm')
    def test_user_get_lesson_page_active_lesson(self, mock_form, mock_lesson_model, mock_goal_model, mock_render):
        factory = RequestFactory()
        request = factory.get('learning-page/lesson/')
        mock_profile = MagicMock()
        mock_goal = MagicMock()
        mock_lesson = MagicMock()
        form = MagicMock()
        request.user = MagicMock()
        request.user.profile = mock_profile

        session = self.client.session
        request.session = session
        session['goal_id'] = 1
        session['active_lesson_id'] = 1
        session.save()

        mock_goal_model.get.return_value = mock_goal
        mock_lesson_model.get.return_value = mock_lesson
        mock_form.return_value = form

        actual_result = LessonPage.as_view()(request)
        mock_lesson_model.get.assert_called_once_with(pk=1)
        mock_render.assert_called_once_with(request, 'lesson.html', {'form': form, 'lesson': mock_lesson})

    @patch('lesson.views.lesson.render')
    @patch('lesson.views.lesson.Goal.objects')
    @patch('lesson.views.lesson.Section.objects')
    @patch('lesson.views.lesson.Theme.objects')
    @patch('lesson.views.lesson.Lesson.objects')
    @patch('lesson.views.lesson.LearningForm')
    @patch('lesson.views.lesson.Question.objects')
    def test_user_post_lesson_page_valid_form(self, mock_question_model,
                                              mock_form, mock_lesson_model,
                                              mock_theme_model, mock_section_model,
                                              mock_goal_model, mock_render):
        factory = RequestFactory()
        request = factory.post('learning-page/lesson/')

        mock_goal = MagicMock()
        mock_section = MagicMock()
        mock_theme = MagicMock()
        mock_lesson = MagicMock()
        mock_question = MagicMock()
        form = MagicMock()
        request.user = MagicMock()

        session = self.client.session
        request.session = session
        session['goal_id'] = 1
        session['lesson_section_id'] = 1
        session['lesson_theme_id'] = 1
        session['active_lesson_id'] = 1
        session.save()

        mock_form.return_value = form  # Класс формы возвращает обект
        mock_form().is_valid.return_value = True
        mock_form().cleaned_data = {'question': 'test_q', 'answer': 'test_a'}  # Объект класса формы
        mock_lesson_model.get.return_value = mock_lesson
        mock_goal_model.get.return_value = mock_goal
        mock_section_model.get.return_value = mock_section
        mock_theme_model.get.return_value = mock_theme
        mock_question_model.create.return_value = mock_question

        actual_result = LessonPage.as_view()(request)
        mock_question_model.create.assert_called_once_with(question='test_q', answer='test_a',
                                                           lesson=mock_lesson, goal=mock_goal,
                                                           section=mock_section, theme=mock_theme)
        mock_render.assert_called_once_with(request, 'lesson.html', {'form': form, 'lesson': mock_lesson})

    @patch('lesson.views.lesson.render')
    @patch('lesson.views.lesson.Goal.objects')
    @patch('lesson.views.lesson.Section.objects')
    @patch('lesson.views.lesson.Theme.objects')
    @patch('lesson.views.lesson.Lesson.objects')
    @patch('lesson.views.lesson.LearningForm')
    @patch('lesson.views.lesson.Question.objects')
    def test_user_post_lesson_page_invalid_form(self, mock_question_model,
                                                mock_form, mock_lesson_model,
                                                mock_theme_model, mock_section_model,
                                                mock_goal_model, mock_render):
        factory = RequestFactory()
        request = factory.post('learning-page/lesson/')

        mock_goal = MagicMock()
        mock_section = MagicMock()
        mock_theme = MagicMock()
        mock_lesson = MagicMock()
        mock_question = MagicMock()
        form = MagicMock()
        request.user = MagicMock()

        session = self.client.session
        request.session = session
        session['goal_id'] = 1
        session['lesson_section_id'] = 1
        session['lesson_theme_id'] = 1
        session['active_lesson_id'] = 1
        session.save()

        mock_form.return_value = form
        mock_form().is_valid.return_value = False
        mock_lesson_model.get.return_value = mock_lesson
        mock_goal_model.get.return_value = mock_goal
        mock_section_model.get.return_value = mock_section
        mock_theme_model.get.return_value = mock_theme
        mock_question_model.create.return_value = mock_question

        actual_result = LessonPage.as_view()(request)
        mock_render.assert_called_once_with(request, 'lesson.html', {'form': form, 'lesson': mock_lesson})

    @patch('lesson.views.lesson.render')
    @patch('lesson.views.lesson.Lesson.objects')
    def test_user_get_end_lesson_page(self, mock_lesson_model, mock_render):
        factory = RequestFactory()
        request = factory.get('learning-page/end-lesson/')

        mock_lesson = MagicMock()
        request.user = MagicMock()

        session = self.client.session
        request.session = session
        session['active_lesson_id'] = 1
        session.save()

        mock_lesson_model.get.return_value = mock_lesson

        actual_result = EndLessonPage.as_view()(request)
        mock_render.assert_called_once_with(request, 'end_lesson.html', {'lesson': mock_lesson})

    @patch('lesson.views.lesson.redirect')
    @patch('lesson.views.lesson.Goal.objects')
    def test_user_post_end_lesson_page_end(self, mock_goal_model, mock_redirect):
        factory = RequestFactory()
        request = factory.post('learning-page/end-lesson/', data={'end': 'End lesson'})

        mock_goal = MagicMock()
        mock_goal.id = 1
        request.user = MagicMock()

        session = self.client.session
        request.session = session
        session['goal_id'] = 1
        session['lesson_section_id'] = 1
        session['lesson_theme_id'] = 1
        session['active_lesson_id'] = 1
        session.save()

        mock_goal_model.get.return_value = mock_goal

        actual_result = EndLessonPage.as_view()(request)
        mock_redirect.assert_called_once_with('memo:goal_page', goal_id=1)

    @patch('lesson.views.lesson.redirect')
    def test_user_post_end_lesson_page_continue(self, mock_redirect):
        factory = RequestFactory()
        request = factory.post('learning-page/end-lesson/', data={'continue': 'continue'})
        request.user = MagicMock()

        actual_result = EndLessonPage.as_view()(request)
        mock_redirect.assert_called_once_with('lesson:lesson_page')
