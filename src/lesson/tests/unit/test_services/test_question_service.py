from datetime import date, timedelta
from unittest.mock import patch, MagicMock

from django.test import SimpleTestCase

from lesson.services import QuestionService


class QuestionServicesTest(SimpleTestCase):
    FILE_PATH = 'lesson.services.question_service'

    def test_calculate_new_cycle_more_then_1_score_less_then_3(self):
        cycle = 2
        score = 2
        result = QuestionService.calculate_new_cycle(cycle, score)
        expected_new_cycle = cycle + 1
        self.assertEqual(result, expected_new_cycle)

    def test_calculate_new_cycle_more_then_1_score_between_3_5(self):
        cycle = 3
        score = 3
        result = QuestionService.calculate_new_cycle(cycle, score)
        expected_new_cycle = cycle - 1
        self.assertEqual(result, expected_new_cycle)

    def test_calculate_new_cycle_more_then_1_score_greater_then_5(self):
        cycle = 2
        score = 7
        result = QuestionService.calculate_new_cycle(cycle, score)
        expected_new_cycle = 1
        self.assertEqual(result, expected_new_cycle)

    def test_calculate_new_cycle_equal_to_1_score_less_then_3(self):
        cycle = 1
        score = 2
        result = QuestionService.calculate_new_cycle(cycle, score)
        expected_new_cycle = cycle + 1
        self.assertEqual(result, expected_new_cycle)

    def test_calculate_new_cycle_equal_to_1_score_greater_then_2(self):
        cycle = 1
        score = 3
        result = QuestionService.calculate_new_cycle(cycle, score)
        expected_new_cycle = cycle
        self.assertEqual(result, expected_new_cycle)

    def test_calculate_new_cycle_equal_to_0_score_greater_then_0(self):
        cycle = 0
        score = 1
        result = QuestionService.calculate_new_cycle(cycle, score)
        expected_new_cycle = 1
        self.assertEqual(result, expected_new_cycle)

    @patch(f'{FILE_PATH}.QuestionService.cycle_to_days')
    @patch(f'{FILE_PATH}.date')
    def test_next_repeat_at_handler(self,  patch_date, patch_cycle_to_days):
        test_days = 3
        test_cycle = 2
        mock_prev_repeat_date = MagicMock()
        patch_date.return_value = mock_prev_repeat_date
        mock_prev_repeat_date.__add__.return_value = mock_prev_repeat_date
        mock_prev_repeat_date.today.return_value = mock_prev_repeat_date
        patch_cycle_to_days.return_value = test_days
        result = QuestionService.next_repeat_at_handler(test_cycle, mock_prev_repeat_date)
        self.assertEqual(result, mock_prev_repeat_date)

    @patch(f'{FILE_PATH}.QuestionService.renew_date_of_all_forgotten_questions')
    @patch(f'{FILE_PATH}.Question.objects.filter')
    def test_get_today_questions_by_profile(self, patch_filter, patch_renew_f_questions):
        test_renewed_questions_num = 3
        test_query = MagicMock()
        test_profile = MagicMock()

        patch_renew_f_questions.return_value = test_renewed_questions_num
        patch_filter.return_value = test_query

        result = QuestionService.get_today_questions_by_profile(test_profile)
        self.assertEqual(result, test_query)
        patch_renew_f_questions.assert_called_once_with(test_profile)
        patch_filter.assert_called_once_with(lesson__goal__profile=test_profile, next_repeat_at=date.today())

    def test_get_next_question_by_rep_session(self):
        test_query = MagicMock()
        expected_question = MagicMock()
        fail_question = MagicMock()
        test_rep_session = MagicMock()

        test_rep_session.questions = test_query
        test_query.filter.return_value = test_query
        test_query.order_by.return_value = test_query
        test_query.first.return_value = expected_question

        result = QuestionService.get_next_question_by_rep_session(test_rep_session)

        test_query.filter.assert_called_once_with(next_repeat_at=date.today())
        test_query.order_by.assert_called_once_with('edited_at')
        test_query.first.assert_called_once()
        self.assertEqual(result, expected_question)
        self.assertNotEqual(result, fail_question)

    @patch(f'{FILE_PATH}.Question.objects.bulk_update')
    @patch(f'{FILE_PATH}.Question.objects.filter')
    def test_renew_date_of_all_forgotten_questions(self, patch_filter, patch_bulk_update):
        test_query = [MagicMock(), MagicMock()]
        test_profile = MagicMock()
        today_date = date.today()
        yesterday_date = today_date - timedelta(days=1)

        patch_filter.return_value = test_query
        patch_bulk_update.return_value = test_query

        result = QuestionService.renew_date_of_all_forgotten_questions(test_profile)

        patch_filter.assert_called_once_with(lesson__goal__profile=test_profile, next_repeat_at__lte=yesterday_date)
        patch_bulk_update.assert_called_once_with(test_query, ['next_repeat_at'])

    @patch(f'{FILE_PATH}.QuestionService.next_repeat_at_handler')
    @patch(f'{FILE_PATH}.QuestionService.calculate_new_cycle')
    def test_save_remembered_question(self, patch_calculate, patch_handler):
        test_cycle = 1
        test_new_cycle = 2
        test_score = 2
        test_prev_repeat_date = MagicMock()
        test_next_repeat_date = MagicMock()
        test_new_repeat_date = MagicMock()
        test_question = MagicMock(cycle=test_cycle,
                                  prev_repeat_at=test_prev_repeat_date,
                                  next_repeat_at=test_next_repeat_date, )

        patch_calculate.return_value = test_new_cycle
        patch_handler.return_value = test_new_repeat_date

        result = QuestionService.save_remembered_question(test_question, test_score)

        patch_calculate.assert_called_once_with(test_cycle, test_score)
        patch_handler.assert_called_once_with(test_new_cycle, test_next_repeat_date)
        test_question.save.assert_called_once()
