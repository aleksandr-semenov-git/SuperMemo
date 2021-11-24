import os

from .test_models import MemoTestCases
from .test_forms import AddGoalFormTest, PersonalDataEditFormTest
from .test_views import ProfilePageTest

os.environ['DJANGO_SETTINGS_MODULE'] = 'src.settings'
