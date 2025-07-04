import factory

from rest_framework.test import APIRequestFactory
from rest_framework_simplejwt.tokens import AccessToken

from django.test import TestCase

from datetime import datetime

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

from .factories import (
    UserFactory,
    CustomerFactory,
    SupplierFactory,
    PayableFactory,
    ReceivableFactory
)

from shared.helpers import get_start_and_end_date


class ReceivableSearchEndpointViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = UserFactory()

        owner = Owner.objects.create(user=self.user)
        self.business = Business.objects.create(
            legal_name='The Test Business INC',
            trade_name='Test Business',
            cnpj=12345678901234
        )
        owner.business = self.business
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

    def test_search_by_name(self):
        customer = CustomerFactory.create(
            name='Customer Name',
            alias='Customer Alias',
        )

        ReceivableFactory.create(
            business=self.business,
            contact=customer,
        )

        request = self.factory.get(
            'receivables/?search=Customer Name',
            HTTP_AUTHORIZATION=self.auth_header
        )
        response = ReceivableSearchEndpoint.as_view()(request)

        receivable_contact = response.data['results'][0]['payment']['contact']
        self.assertEqual(receivable_contact, 'Customer Name')

    def test_search_by_alias(self):
        customer = CustomerFactory.create(
            name='Customer Name',
            alias='Customer Alias',
        )

        ReceivableFactory.create(
            business=self.business,
            contact=customer,
        )

        request = self.factory.get(
            'receivables/?search=Customer Alias',
            HTTP_AUTHORIZATION=self.auth_header
        )
        response = ReceivableSearchEndpoint.as_view()(request)
        
        receivable_contact = response.data['results'][0]['payment']['contact']
        self.assertEqual(receivable_contact, 'Customer Name')

    def test_search_by_reference(self):
        customer = CustomerFactory.create(
            name='Customer Name',
            alias='Customer Alias',
        )

        ReceivableFactory.create(
            business=self.business,
            contact=customer,
            reference='Customer Recivable Ref'
        )

        request = self.factory.get(
            'receivables/?search=Customer Recivable Ref',
            HTTP_AUTHORIZATION=self.auth_header
        )
        response = ReceivableSearchEndpoint.as_view()(request)
        
        receivable_ref = response.data['results'][0]['payment']['reference']
        self.assertEqual(receivable_ref, 'Customer Recivable Ref')

    def test_search_by_notes(self):
        customer = CustomerFactory.create(
            name='Customer Name',
            alias='Customer Alias',
        )

        ReceivableFactory.create(
            business=self.business,
            contact=customer,
            notes='Customer Recivable Notes'
        )

        request = self.factory.get(
            'receivables/?search=Customer Recivable Notes',
            HTTP_AUTHORIZATION=self.auth_header
        )
        response = ReceivableSearchEndpoint.as_view()(request)
        
        receivable_notes = response.data['results'][0]['payment']['notes']
        self.assertEqual(receivable_notes, 'Customer Recivable Notes')


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
        self.account = FinancialAccount.objects.create(
            name='Bank', business=business
        )

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
        self.business = Business.objects.create(
            legal_name='The Test Business INC',
            trade_name='Test Business',
            cnpj=12345678901234
        )
        owner.business = self.business
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

    def test_search_by_legal_name(self):
        supplier = SupplierFactory.create(
            legal_name='Legal Name',
            trade_name='Trade Name',
        )

        PayableFactory.create(business=self.business, contact=supplier)

        request = self.factory.get(
            'payables/?search=Legal Name',
            HTTP_AUTHORIZATION=self.auth_header
        )
        response = PayableSearchEndpoint.as_view()(request)
        
        payable_contact = response.data['results'][0]['payment']['contact']
        self.assertEqual(payable_contact, 'Legal Name')

    def test_search_by_trade_name(self):
        supplier = SupplierFactory.create(
            legal_name='Legal Name',
            trade_name='Trade Name',
        )

        PayableFactory.create(business=self.business, contact=supplier)

        request = self.factory.get(
            'payables/?search=Trade Name',
            HTTP_AUTHORIZATION=self.auth_header
        )
        response = PayableSearchEndpoint.as_view()(request)
        
        payable_contact = response.data['results'][0]['payment']['contact']
        self.assertEqual(payable_contact, 'Legal Name')

    def test_search_by_reference(self):
        supplier = SupplierFactory.create(
            legal_name='Legal Name',
            trade_name='Trade Name',
        )

        PayableFactory.create(
            business=self.business,
            contact=supplier,
            reference='Reference Test 01',
        )

        request = self.factory.get(
            'payables/?search=Reference Test 01',
            HTTP_AUTHORIZATION=self.auth_header
        )
        response = PayableSearchEndpoint.as_view()(request)
        
        payable_ref = response.data['results'][0]['payment']['reference']
        self.assertEqual(payable_ref, 'Reference Test 01')

    def test_search_by_notes(self):
        supplier = SupplierFactory.create(
            legal_name='Legal Name',
            trade_name='Trade Name',
        )

        PayableFactory.create(
            business=self.business,
            contact=supplier,
            notes='Payable note',
        )

        request = self.factory.get(
            'payables/?search=Payable note',
            HTTP_AUTHORIZATION=self.auth_header
        )
        response = PayableSearchEndpoint.as_view()(request)
        
        payable_notes = response.data['results'][0]['payment']['notes']
        self.assertEqual(payable_notes, 'Payable note')


    def test_invalid_date_format(self):
        request = self.factory.get(
            'payables/?date=2025-03-001',
            HTTP_AUTHORIZATION=self.auth_header
        )
        response = PayableSearchEndpoint.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_start_and_end_week_dates(self):
        '''
        The `?date=week` query param returns all dates in the
        current week, starting Sunday and ending on Saturday.
        '''
        today = datetime.now()
        start_date, end_date = get_start_and_end_date(today, week=True)

        supplier = SupplierFactory.create()
        PayableFactory.create_batch(
            2,
            business=self.business,
            contact=supplier,
            due_at=factory.Iterator([start_date, end_date]),
        )

        request = self.factory.get(
            'payables/?date=week',
            HTTP_AUTHORIZATION=self.auth_header
        )
        response = PayableSearchEndpoint.as_view()(request)

        payable_0001_due_date = response.data['results'][0]['payment']['due_at']
        payable_0002_due_date = response.data['results'][1]['payment']['due_at']
        self.assertEqual(payable_0001_due_date, start_date.strftime('%Y-%m-%d'))
        self.assertEqual(payable_0002_due_date, end_date.strftime('%Y-%m-%d'))


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

