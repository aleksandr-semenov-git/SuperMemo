from functools import wraps

from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.views import View


class TestMixin1(UserPassesTestMixin):

    def __init__(self, request, *args, **kwargs):
        self.session = request.session

    def test_func(self):
        if self.session['active_lesson_id']:
            return redirect('lesson:lesson_page')


# def is_active_lesson(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
#     """
#     Decorator for views that checks that the user is logged in, redirecting
#     to the log-in page if necessary.
#     """
#     actual_decorator = user_passes_test(
#         lambda u: u.is_authenticated,
#         login_url=login_url,
#         redirect_field_name=redirect_field_name
#     )
#     if function:
#         return actual_decorator(function)
#     return actual_decorator