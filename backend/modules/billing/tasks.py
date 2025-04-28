from celery import shared_task

from datetime import date

from .models import Payment


@shared_task
def update_payment_status():
    now = date.today()
    payments = Payment.objects.all()
    for payment in payments:
        if payment.status != 'paid':
            if payment.due_at < now:
                payment.status = 'overdue'
            payment.save()
    return 'Update payment task completed'