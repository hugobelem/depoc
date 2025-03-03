from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum

from datetime import date, timedelta
from dateutil.relativedelta import relativedelta, MO, TU, WE, TH, FR, SA, SU

import ulid

from modules.finance.models import FinancialTransaction

from .models import Payment


def count_weekdays(start_date: date, weekday: str):
    weekdays = [
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
    ]

    weekday_to_int = weekdays.index(weekday)
    
    end_date = date(start_date.year, 12, 31)
    count = 0
    while start_date <= end_date:
        if start_date.weekday() == weekday_to_int:
            count += 1
        start_date += timedelta(days=1)
    return count


def count_months(due_date: date):
    end_date = date(due_date.year, 12, 31)
    count = 0
    
    while due_date <= end_date:
        count += 1
        due_date += relativedelta(months=1)

    return count


def create_installment(
        payment: Payment,
        due_date: date,
        due_day: date | None = None,
        due_weekday: date | None = None,
        weeks: int | None = None,
        months: int | None = None,
        count: int | None = None,
        installments: int | None = None,
        is_weekly=False,
        is_monthly=False,
        is_installments=False,
    ):

    weekday_map = {
        "monday": MO,
        "tuesday": TU,
        "wednesday": WE,
        "thursday": TH,
        "friday": FR,
        "saturday": SA,
        "sunday": SU,
    }

    notes = payment.notes

    if is_installments:
        notes = f'{payment.notes} | instalment [{count} of {installments}]'
        next_due_date = due_date.replace(day=due_day) + relativedelta(months=months)
    elif is_weekly:
        next_weekday = due_date + relativedelta(weekday=weekday_map[due_weekday])
        next_due_date = next_weekday + timedelta(weeks=weeks)
    elif is_monthly:
        next_due_date = due_date + relativedelta(months=months)

    return Payment(
        id = ulid.new().str,
        contact=payment.contact,
        category=payment.category,
        business=payment.business,
        issued_at=payment.issued_at,
        due_at=next_due_date,
        total_amount=payment.total_amount,
        status='pending',
        paid_at=None,
        payment_method=payment.payment_method,
        reference=payment.reference,
        notes=notes,
        recurrence='once',
        installment_count=0,
        payment_type=payment.payment_type,
    )


@receiver(pre_save, sender=Payment)
def generate_ulids(sender, instance, **kwargs):
    if not instance.id:
        instance.id = ulid.new().str


@receiver(post_save, sender=Payment)
def generate_installments(sender, instance, created, **kwargs):
    recurrence = instance.recurrence
    if created and recurrence == 'installments':
        installment_count = instance.installment_count
        due_day: date = instance.due_day_of_month
        due_at: date = instance.due_at

        count = 1
        months = 0
        installment_payments = []
        for _ in range(1, installment_count):
            count += 1
            months += 1
            installment_payments.append(
                create_installment(
                    payment=instance,
                    due_at=due_at,
                    due_day=due_day,
                    months=months,
                    count=count,
                    installment_count=installment_count,
                    is_installments=True,
                )
            )

        if installment_payments:
            Payment.objects.bulk_create(installment_payments)

        instance.notes = f'{instance.notes} | instalment [{1} of {installment_count}]'
        instance.installment_count = 0
        instance.recurrence = 'once'
        instance.save()


@receiver(post_save, sender=Payment)
def generate_weekly_payments(sender, instance, created, **kwargs):
    recurrence = instance.recurrence
    if created and recurrence == 'weekly':
        due_date = instance.due_date_of_month
        due_weekday = instance.due_weekday

        weekdays_left = count_weekdays(due_date, due_weekday)
        weekly_payments = []
        for week in range(1, weekdays_left):
            weekly_payments.append(
                create_installment(
                    payment=instance,
                    due_date=due_date,
                    due_weekday=due_weekday,
                    weeks=week,
                    is_weekly=True,
                )
            )

        if weekly_payments:
            Payment.objects.bulk_create(weekly_payments)

        instance.recurrence = 'once'
        instance.save()


@receiver(post_save, sender=Payment)
def generate_monthly_payments(sender, instance, created, **kwargs):
    recurrence = instance.recurrence
    if created and recurrence == 'monthly':
        due_date = instance.due_date_of_month
        months_left = count_months(due_date)

        monthly_payments = []
        for month in range(1, months_left):
            monthly_payments.append(
                create_installment(
                    payment=instance,
                    due_date=due_date,
                    months=month,
                    is_monthly=True
                )
            )

        if monthly_payments:
            Payment.objects.bulk_create(monthly_payments)

        instance.recurrence = 'once'
        instance.save()


@receiver(post_delete, sender=FinancialTransaction)
@receiver(post_save, sender=FinancialTransaction)
def update_payment_balance(sender, instance, **kwargs):
    payment = instance.payment
    if payment:
        total_amount = payment.total_amount

        total_amount_paid = FinancialTransaction.objects\
            .filter(payment=payment)\
            .aggregate((Sum('amount')))['amount__sum'] or 0
        
        payment.amount_paid = abs(total_amount_paid)
        payment.outstanding_balance = total_amount - abs(total_amount_paid)
        payment.save()


@receiver(post_save, sender=Payment)
def update_outstanding_balance(sender, instance, created, **kwargs):
    if created:
        instance.outstanding_balance = instance.total_amount
        instance.save()


@receiver(post_delete, sender=FinancialTransaction)
@receiver(post_save, sender=FinancialTransaction)
def update_payment_status(sender, instance, **kwargs):
    payment = instance.payment
    if payment:
        total_amount = payment.total_amount
        amount_paid = payment.amount_paid

        if amount_paid == 0:
            payment.status = 'pending'
        elif amount_paid != 0 and amount_paid < total_amount:
            payment.status = 'partially_paid'
        elif amount_paid >= total_amount:
            payment.status = 'paid'

        payment.save()
