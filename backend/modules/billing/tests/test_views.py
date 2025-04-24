from rest_framework.test import APIRequestFactory
from rest_framework_simplejwt.tokens import AccessToken

from django.test import TestCase

from modules.billing.views import (
    ReceivableSearchEndpoint,
    ReceivablesEndpoint,
    ReceivableSettleEndpoint,
    PayableSearchEndpoint,
    PayablesEndpoint,
    PayableSettleEndpoint,
)

from modules.accounts.models import Owner
from modules.business.models import Business
from modules.finance.models import FinancialAccount
from modules.billing.models import Payment

from .factories import UserFactory, CustomerFactory


class ReceivableSearchEndpointViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = UserFactory()

        owner = Owner.objects.create(user=self.user)
        business = Business.objects.create(
            legal_name='The Test Business INC',
            trade_name='Test Business',
            cnpj=12345678901234
        )
        owner.business = business
        owner.save()

        self.token = AccessToken.for_user(self.user)
        self.auth_header = f'Bearer {self.token}'

    def test_permission_is_admin(self):
        self.user.is_staff = False
        self.user.save()
        request = self.factory.get(
            'receivables/?search=abc',
            HTTP_AUTHORIZATION=self.auth_header
        )
        response = ReceivableSearchEndpoint.as_view()(request)
        self.assertEqual(response.status_code, 403)

    def test_invalid_query_params(self):
        request = self.factory.get(
            'receivables/?dats',
            HTTP_AUTHORIZATION=self.auth_header
        )
        response = ReceivableSearchEndpoint.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_length_search_query_param(self):
        request = self.factory.get(
            'receivables/?search=ab',
            HTTP_AUTHORIZATION=self.auth_header
        )
        response = ReceivableSearchEndpoint.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_invalid_date_format(self):
        request = self.factory.get(
            'receivables/?date=2025-03-001',
            HTTP_AUTHORIZATION=self.auth_header
        )
        response = ReceivableSearchEndpoint.as_view()(request)
        self.assertEqual(response.status_code, 400)


class ReceivablesEndpointViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = UserFactory()
        self.customer = CustomerFactory()

        owner = Owner.objects.create(user=self.user)
        business = Business.objects.create(
            legal_name='The Test Business INC',
            trade_name='Test Business',
            cnpj=12345678901234
        )
        owner.business = business
        owner.save()
        self.account = FinancialAccount.objects.create(name='Bank', business=business)

        self.token = AccessToken.for_user(self.user)
        self.auth_header = f'Bearer {self.token}'

    def test_permission_is_admin(self):
        self.user.is_staff = False
        self.user.save()
        request = self.factory.get(
            'receivables',
            HTTP_AUTHORIZATION=self.auth_header,
        )
        response = ReceivablesEndpoint.as_view()(request)
        self.assertEqual(response.status_code, 403)

    def test_create_receivable_recurrence_once(self):
        data = {
            'contact': self.customer.id,
            'issued_at': '2025-04-21',
            'due_at': '2025-05-25',
            'total_amount': '1000',
            'payment_method': 'Cash',
            'recurrence': 'once',
            'reference': '12304923',
            'notes': 'To be received by Foo',
        }
        request = self.factory.post(
            'receivables',
            data=data,
            HTTP_AUTHORIZATION=self.auth_header,
        )
        response = ReceivablesEndpoint.as_view()(request)
        self.assertEqual(response.status_code, 201)

    def test_create_receivable_recurrence_weekly(self):
        data = {
            'contact': self.customer.id,
            'issued_at': '2025-04-21',
            'due_at': '2025-05-25',
            'total_amount': '1000',
            'payment_method': 'Cash',
            'recurrence': 'weekly',
            'due_weekday': 'monday',
            'reference': '12304923',
            'notes': 'To be received by Foo',
        }
        request = self.factory.post(
            'receivables',
            data=data,
            HTTP_AUTHORIZATION=self.auth_header,
        )
        response = ReceivablesEndpoint.as_view()(request)
        self.assertEqual(response.status_code, 201)

    def test_create_receivable_recurrence_monthly(self):
        data = {
            'contact': self.customer.id,
            'issued_at': '2025-04-21',
            'due_at': '2025-05-25',
            'total_amount': '1000',
            'payment_method': 'Cash',
            'recurrence': 'monthly',
            'reference': '12304923',
            'notes': 'To be received by Foo',
        }
        request = self.factory.post(
            'receivables',
            data=data,
            HTTP_AUTHORIZATION=self.auth_header,
        )
        response = ReceivablesEndpoint.as_view()(request)
        self.assertEqual(response.status_code, 201)

    def test_create_receivable_recurrence_installments(self):
        data = {
            'contact': self.customer.id,
            'issued_at': '2025-04-21',
            'due_at': '2025-05-25',
            'total_amount': '1000',
            'payment_method': 'Cash',
            'recurrence': 'installments',
            'installment_count': 5,
            'due_day_of_month': 1,
            'reference': '12304923',
            'notes': 'To be received by Foo',
        }
        request = self.factory.post(
            'receivables',
            data=data,
            HTTP_AUTHORIZATION=self.auth_header,
        )
        response = ReceivablesEndpoint.as_view()(request)
        self.assertEqual(response.status_code, 201)
    
    def test_change_outstanding_balance_on_total_amount_update(self):
        data = {
            'contact': self.customer.id,
            'issued_at': '2025-04-21',
            'due_at': '2025-05-25',
            'total_amount': '1000',
            'payment_method': 'Cash',
            'recurrence': 'installments',
            'installment_count': 5,
            'due_day_of_month': 1,
            'reference': '12304923',
            'notes': 'To be received by Foo',
        }
        request = self.factory.post(
            'receivables',
            data=data,
            HTTP_AUTHORIZATION=self.auth_header,
        )
        response = ReceivablesEndpoint.as_view()(request)
        payment = response.data['payment']
        self.assertEqual(payment['outstanding_balance'], '1000.00')

        request = self.factory.patch(
            'receivables/<id>',
            data={'total_amount': 50},
            HTTP_AUTHORIZATION=self.auth_header,
        )
        response = ReceivablesEndpoint.as_view()(
            request,
            receivable_id=payment['id']
        )
        payment = response.data['payment']
        self.assertEqual(payment['outstanding_balance'], '50.00')

    def test_receivable_pending_status(self):
        data = {
            'contact': self.customer.id,
            'issued_at': '2025-04-21',
            'due_at': '2025-05-25',
            'total_amount': '1000',
            'payment_method': 'Cash',
            'recurrence': 'installments',
            'installment_count': 5,
            'due_day_of_month': 1,
            'reference': '12304923',
            'notes': 'To be received by Foo',
        }
        request = self.factory.post(
            'receivables',
            data=data,
            HTTP_AUTHORIZATION=self.auth_header,
        )
        response = ReceivablesEndpoint.as_view()(request)
        payment = response.data['payment']
        self.assertEqual(payment['status'], 'pending')
        self.assertEqual(payment['amount_paid'], '0.00')

    def test_receivable_partially_paid_status(self):
        data = {
            'contact': self.customer.id,
            'issued_at': '2025-04-21',
            'due_at': '2025-05-25',
            'total_amount': '100',
            'payment_method': 'Cash',
            'recurrence': 'installments',
            'installment_count': 5,
            'due_day_of_month': 1,
            'reference': '12304923',
            'notes': 'To be received by Foo',
        }
        request = self.factory.post(
            'receivables',
            data=data,
            HTTP_AUTHORIZATION=self.auth_header,
        )
        create_receivable_response = ReceivablesEndpoint.as_view()(request)

        request = self.factory.post(
            'receivables/settle/<id>',
            data={'amount': 25, 'account': f'{self.account.id}'},
            HTTP_AUTHORIZATION=self.auth_header,
        )

        receivable_id = create_receivable_response.data['payment']['id']
        settle_receivable_response = ReceivableSettleEndpoint.as_view()(
            request,
            receivable_id=receivable_id
        )

        receivable = Payment.objects.get(id=receivable_id)
        self.assertEqual(receivable.status, 'partially_paid')
        self.assertEqual(receivable.amount_paid, 25.00)
        self.assertEqual(receivable.outstanding_balance, 75.00)

    def test_delete_receivable_with_associated_transaction(self):
        data = {
            'contact': self.customer.id,
            'issued_at': '2025-04-21',
            'due_at': '2025-05-25',
            'total_amount': '100',
            'payment_method': 'Cash',
            'recurrence': 'installments',
            'installment_count': 5,
            'due_day_of_month': 1,
            'reference': '12304923',
            'notes': 'To be received by Foo',
        }
        request = self.factory.post(
            'receivables',
            data=data,
            HTTP_AUTHORIZATION=self.auth_header,
        )
        create_receivable_response = ReceivablesEndpoint.as_view()(request)

        request = self.factory.post(
            'receivables/settle/<id>',
            data={'amount': 25, 'account': f'{self.account.id}'},
            HTTP_AUTHORIZATION=self.auth_header,
        )

        receivable_id = create_receivable_response.data['payment']['id']
        settle_receivable_response = ReceivableSettleEndpoint.as_view()(
            request,
            receivable_id=receivable_id
        )

        request = self.factory.delete(
            'receivable',
            HTTP_AUTHORIZATION=self.auth_header,
        )

        delete_receivable_response = ReceivablesEndpoint.as_view()(
            request,
            receivable_id=receivable_id
        )

        error_message = (
            'Cannot delete receivable because it has '
            'associated financial transactions.'
        )
        self.assertEqual(delete_receivable_response.status_code, 500)
        self.assertEqual(
            delete_receivable_response.data['error']['message'], error_message
        )


class PayableSearchEndpointViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = UserFactory()

        owner = Owner.objects.create(user=self.user)
        business = Business.objects.create(
            legal_name='The Test Business INC',
            trade_name='Test Business',
            cnpj=12345678901234
        )
        owner.business = business
        owner.save()

        self.token = AccessToken.for_user(self.user)
        self.auth_header = f'Bearer {self.token}'

    def test_permission_is_admin(self):
        self.user.is_staff = False
        self.user.save()
        request = self.factory.get(
            'payables/?search=abc',
            HTTP_AUTHORIZATION=self.auth_header
        )
        response = PayableSearchEndpoint.as_view()(request)
        self.assertEqual(response.status_code, 403)

    def test_invalid_query_params(self):
        request = self.factory.get(
            'payables/?dats',
            HTTP_AUTHORIZATION=self.auth_header
        )
        response = PayableSearchEndpoint.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_length_search_query_param(self):
        request = self.factory.get(
            'payables/?search=ab',
            HTTP_AUTHORIZATION=self.auth_header
        )
        response = PayableSearchEndpoint.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_invalid_date_format(self):
        request = self.factory.get(
            'payables/?date=2025-03-001',
            HTTP_AUTHORIZATION=self.auth_header
        )
        response = PayableSearchEndpoint.as_view()(request)
        self.assertEqual(response.status_code, 400)


class PayablesEndpointViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = UserFactory()
        self.customer = CustomerFactory()

        owner = Owner.objects.create(user=self.user)
        business = Business.objects.create(
            legal_name='The Test Business INC',
            trade_name='Test Business',
            cnpj=12345678901234
        )
        owner.business = business
        owner.save()
        self.account = FinancialAccount.objects.create(name='Bank', business=business)

        self.token = AccessToken.for_user(self.user)
        self.auth_header = f'Bearer {self.token}'

    def test_permission_is_admin(self):
        self.user.is_staff = False
        self.user.save()
        request = self.factory.get(
            'payables',
            HTTP_AUTHORIZATION=self.auth_header,
        )
        response = PayablesEndpoint.as_view()(request)
        self.assertEqual(response.status_code, 403)

    def test_create_payable_recurrence_once(self):
        data = {
            'contact': self.customer.id,
            'issued_at': '2025-04-21',
            'due_at': '2025-05-25',
            'total_amount': '1000',
            'payment_method': 'Cash',
            'recurrence': 'once',
            'reference': '12304923',
            'notes': 'To be received by Foo',
        }
        request = self.factory.post(
            'payables',
            data=data,
            HTTP_AUTHORIZATION=self.auth_header,
        )
        response = PayablesEndpoint.as_view()(request)
        self.assertEqual(response.status_code, 201)

    def test_create_payable_recurrence_weekly(self):
        data = {
            'contact': self.customer.id,
            'issued_at': '2025-04-21',
            'due_at': '2025-05-25',
            'total_amount': '1000',
            'payment_method': 'Cash',
            'recurrence': 'weekly',
            'due_weekday': 'monday',
            'reference': '12304923',
            'notes': 'To be received by Foo',
        }
        request = self.factory.post(
            'payables',
            data=data,
            HTTP_AUTHORIZATION=self.auth_header,
        )
        response = PayablesEndpoint.as_view()(request)
        self.assertEqual(response.status_code, 201)

    def test_create_payable_recurrence_monthly(self):
        data = {
            'contact': self.customer.id,
            'issued_at': '2025-04-21',
            'due_at': '2025-05-25',
            'total_amount': '1000',
            'payment_method': 'Cash',
            'recurrence': 'monthly',
            'reference': '12304923',
            'notes': 'To be received by Foo',
        }
        request = self.factory.post(
            'payables',
            data=data,
            HTTP_AUTHORIZATION=self.auth_header,
        )
        response = PayablesEndpoint.as_view()(request)
        self.assertEqual(response.status_code, 201)

    def test_create_payable_recurrence_installments(self):
        data = {
            'contact': self.customer.id,
            'issued_at': '2025-04-21',
            'due_at': '2025-05-25',
            'total_amount': '1000',
            'payment_method': 'Cash',
            'recurrence': 'installments',
            'installment_count': 5,
            'due_day_of_month': 1,
            'reference': '12304923',
            'notes': 'To be received by Foo',
        }
        request = self.factory.post(
            'payables',
            data=data,
            HTTP_AUTHORIZATION=self.auth_header,
        )
        response = PayablesEndpoint.as_view()(request)
        self.assertEqual(response.status_code, 201)
    
    def test_change_outstanding_balance_on_total_amount_update(self):
        data = {
            'contact': self.customer.id,
            'issued_at': '2025-04-21',
            'due_at': '2025-05-25',
            'total_amount': '1000',
            'payment_method': 'Cash',
            'recurrence': 'installments',
            'installment_count': 5,
            'due_day_of_month': 1,
            'reference': '12304923',
            'notes': 'To be received by Foo',
        }
        request = self.factory.post(
            'payables',
            data=data,
            HTTP_AUTHORIZATION=self.auth_header,
        )
        response = PayablesEndpoint.as_view()(request)
        payment = response.data['payment']
        self.assertEqual(payment['outstanding_balance'], '1000.00')

        request = self.factory.patch(
            'payables/<id>',
            data={'total_amount': 50},
            HTTP_AUTHORIZATION=self.auth_header,
        )
        response = PayablesEndpoint.as_view()(
            request,
            payable_id=payment['id']
        )
        payment = response.data['payment']
        self.assertEqual(payment['outstanding_balance'], '50.00')

    def test_payable_pending_status(self):
        data = {
            'contact': self.customer.id,
            'issued_at': '2025-04-21',
            'due_at': '2025-05-25',
            'total_amount': '1000',
            'payment_method': 'Cash',
            'recurrence': 'installments',
            'installment_count': 5,
            'due_day_of_month': 1,
            'reference': '12304923',
            'notes': 'To be received by Foo',
        }
        request = self.factory.post(
            'payables',
            data=data,
            HTTP_AUTHORIZATION=self.auth_header,
        )
        response = PayablesEndpoint.as_view()(request)
        payment = response.data['payment']
        self.assertEqual(payment['status'], 'pending')
        self.assertEqual(payment['amount_paid'], '0.00')

    def test_payable_partially_paid_status(self):
        data = {
            'contact': self.customer.id,
            'issued_at': '2025-04-21',
            'due_at': '2025-05-25',
            'total_amount': '100',
            'payment_method': 'Cash',
            'recurrence': 'installments',
            'installment_count': 5,
            'due_day_of_month': 1,
            'reference': '12304923',
            'notes': 'To be received by Foo',
        }
        request = self.factory.post(
            'payables',
            data=data,
            HTTP_AUTHORIZATION=self.auth_header,
        )
        create_payable_response = PayablesEndpoint.as_view()(request)

        request = self.factory.post(
            'payables/settle/<id>',
            data={'amount': 25, 'account': f'{self.account.id}'},
            HTTP_AUTHORIZATION=self.auth_header,
        )

        payable_id = create_payable_response.data['payment']['id']
        settle_payable_response = PayableSettleEndpoint.as_view()(
            request,
            payable_id=payable_id
        )

        payable = Payment.objects.get(id=payable_id)
        self.assertEqual(payable.status, 'partially_paid')
        self.assertEqual(payable.amount_paid, 25.00)
        self.assertEqual(payable.outstanding_balance, 75.00)

    def test_delete_payable_with_associated_transaction(self):
        data = {
            'contact': self.customer.id,
            'issued_at': '2025-04-21',
            'due_at': '2025-05-25',
            'total_amount': '100',
            'payment_method': 'Cash',
            'recurrence': 'installments',
            'installment_count': 5,
            'due_day_of_month': 1,
            'reference': '12304923',
            'notes': 'To be received by Foo',
        }
        request = self.factory.post(
            'payable',
            data=data,
            HTTP_AUTHORIZATION=self.auth_header,
        )
        create_payable_response = PayablesEndpoint.as_view()(request)

        request = self.factory.post(
            'payables/settle/<id>',
            data={'amount': 25, 'account': f'{self.account.id}'},
            HTTP_AUTHORIZATION=self.auth_header,
        )

        payable_id = create_payable_response.data['payment']['id']
        settle_payable_response = PayableSettleEndpoint.as_view()(
            request,
            payable_id=payable_id
        )

        request = self.factory.delete(
            'receivable',
            HTTP_AUTHORIZATION=self.auth_header,
        )

        delete_payaable_response = PayablesEndpoint.as_view()(
            request,
            payable_id=payable_id
        )

        error_message = (
            'Cannot delete payable because it has '
            'associated financial transactions.'
        )
        self.assertEqual(delete_payaable_response.status_code, 500)
        self.assertEqual(
            delete_payaable_response.data['error']['message'], error_message
        )

