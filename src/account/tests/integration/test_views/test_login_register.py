from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from django.contrib.auth.models import User
from account.forms import LoginForm, RegistrationForm
from memo.tests.factories import UserFactory, ProfileFactory, GoalFactory, SectionFactory, ThemeFactory, LessonFactory,\
    QuestionFactory


class AccountPagesTest(TestCase):
    FILE_PATH = 'account.views.login_register'

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.user = UserFactory()
        self.user.set_password('121212test')
        self.user.save()
        self.profile = ProfileFactory(user=self.user)
        self.goal = GoalFactory(profile=self.profile)
        self.goal2 = GoalFactory(profile=self.profile)

        self.not_active_user = User.objects.create(username='not_active_user',
                                                   email='testemail@test.test',
                                                   )
        self.not_active_user.set_password('121212test')
        self.not_active_user.save()
        self.not_active_user.is_active = False
        self.not_active_user.save()

    def test_get_login_page(self):
        result = self.client.get(reverse('account:login'), data={})
        self.assertEqual(result.status_code, 200)
        self.assertTemplateUsed(result, 'login.html')
        self.assertTrue(isinstance(result.context['form'], LoginForm))

    def test_post_login_page_success(self):
        result = self.client.post(reverse('account:login'), data={'username': 'test_user0', 'password': '121212test'})
        self.assertEqual(result.status_code, 302)
        self.assertRedirects(result, reverse('account:profile', kwargs={'username': 'test_user0'}))
        self.assertEqual(self.client.session['user_id'], self.user.id)

    def test_post_login_page_invalid_form(self):
        result = self.client.post(reverse('account:login'), data={'username': 'fail_user0', 'password': '121212test'})
        self.assertEqual(result.status_code, 200)
        self.assertTemplateUsed(result, 'login.html')
        self.assertTrue(isinstance(result.context['form'], LoginForm))
        self.assertFormError(result, 'form', None, 'User with login fail_user0 not found.')
        # errors=None mean that formset.non_form_errors()) will be checked

    # def test_post_login_page_inactive_user(self):
    #     result = self.client.post(reverse('account:login'), data={'username': 'not_active_user',
    #                                                               'password': '121212test'})
    #     self.assertEqual(result.content, 'Disabled account')  # Todo: fix
    #
    # def test_post_login_page_user_is_none(self):
    #     result = self.client.post(reverse('account:login'), data={'username': 'fail_username',
    #                                                               'password': '121212test'})
    #     self.assertEqual(result.content, 'Invalid login')    # Todo: fix

    def test_get_logout_view(self):
        result = self.client.get(reverse('account:logout'), data={})
        self.assertRedirects(result, reverse('memo:home'))

    def test_get_register_page(self):
        result = self.client.get(reverse('account:registration'), data={})
        self.assertEqual(result.status_code, 200)
        self.assertTemplateUsed(result, 'registration/registration.html')
        self.assertTrue(isinstance(result.context['form'], RegistrationForm))

    def test_post_register_page_success(self):
        result = self.client.post(reverse('account:registration'), data={'username': 'new_user0',
                                                                         'email': 'new@test.email',
                                                                         'password': '121212test',
                                                                         'confirm_password': '121212test'})
        self.assertRedirects(result, reverse('account:profile', kwargs={'username': 'new_user0'}))

    def test_post_register_page_short_username(self):
        invalid_username = 'xx'
        result = self.client.post(reverse('account:registration'), data={'username': invalid_username,
                                                                         'email': 'new@test.email',
                                                                         'password': '121212test',
                                                                         'confirm_password': '121212test'})
        self.assertEqual(result.status_code, 200)
        self.assertTemplateUsed(result, 'registration/registration.html')
        self.assertTrue(isinstance(result.context['form'], RegistrationForm))
        self.assertFormError(result, 'form', 'username', 'Ensure this value has at least 3 characters (it has 2).')

    def test_post_register_page_username_already_exist(self):
        result = self.client.post(reverse('account:registration'), data={'username': 'test_user0',
                                                                         'email': 'new@test.email',
                                                                         'password': '121212test',
                                                                         'confirm_password': '121212test'})
        self.assertEqual(result.status_code, 200)
        self.assertTemplateUsed(result, 'registration/registration.html')
        self.assertTrue(isinstance(result.context['form'], RegistrationForm))
        self.assertFormError(result, 'form', 'username', 'Current username test_user0 is already registered')

    def test_post_register_page_email_net_domain(self):
        with self.assertNumQueries(1):
            result = self.client.post(reverse('account:registration'), data={'username': 'new_user0',
                                                                             'email': 'new@test.net',
                                                                             'password': '121212test',
                                                                             'confirm_password': '121212test'})
        self.assertEqual(result.status_code, 200)
        self.assertTemplateUsed(result, 'registration/registration.html')
        self.assertTrue(isinstance(result.context['form'], RegistrationForm))
        self.assertFormError(result, 'form', 'email', 'Registration for domain "net" is impossible')

    def test_post_register_page_email_exist(self):
        with self.assertNumQueries(2):
            result = self.client.post(reverse('account:registration'), data={'username': 'new_user0',
                                                                             'email': 'test@test.email',
                                                                             'password': '121212test',
                                                                             'confirm_password': '121212test'})
        self.assertEqual(result.status_code, 200)
        self.assertTemplateUsed(result, 'registration/registration.html')
        self.assertTrue(isinstance(result.context['form'], RegistrationForm))
        self.assertFormError(result, 'form', 'email', 'Current email is already registered')

    def test_post_register_page_password1_is_not_password2(self):
        with self.assertNumQueries(2):
            result = self.client.post(reverse('account:registration'), data={'username': 'new_user0',
                                                                             'email': 'new@test.test',
                                                                             'password': '121212test',
                                                                             'confirm_password': '121212xxxx'})
        self.assertEqual(result.status_code, 200)
        self.assertTemplateUsed(result, 'registration/registration.html')
        self.assertTrue(isinstance(result.context['form'], RegistrationForm))
        # Todo: How to check password form error?

    # def test_post_register_page_inactive_user(self):
    #     result = self.client.post(reverse('account:login'), data={'username': 'not_active_user',
    #                                                               'password': '121212test'})
    #     self.assertEqual(result.content, 'Disabled account')  # Todo: fix
    #
    # def test_post_register_page_user_is_none(self):
    #     result = self.client.post(reverse('account:login'), data={'username': 'fail_username',
    #                                                               'password': '121212test'})
    #     self.assertEqual(result.content, 'Invalid login')    # Todo: fix
