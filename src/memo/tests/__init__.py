import os

from .old_test_models import MemoTestCases
from .old_test_forms import AddGoalFormTest, PersonalDataEditFormTest
from .old_test_views import ProfilePageTest

os.environ['DJANGO_SETTINGS_MODULE'] = 'src.settings'
