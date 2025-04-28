from django.test import TestCase, override_settings

from unittest.mock import patch

from .. import tasks


@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
class UpdatePaymentStatus(TestCase):
    def test_update_payment_status_execution(self):
        result = tasks.update_payment_status.apply()
        self.assertTrue(result.successful())
        self.assertEqual(result.result, 'Update payment task completed')

    @patch('modules.billing.tasks.update_payment_status.delay')
    def test_update_payment_status_scheduling(self, mocked_test):
        tasks.update_payment_status.delay()
        mocked_test.assert_called_once()
