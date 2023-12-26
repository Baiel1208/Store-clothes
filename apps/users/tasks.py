import uuid
from datetime import timedelta

from celery import shared_task
from django.utils.timezone import now

from . import models as m

@shared_task
def send_emailverication(user_id):
    user = m.User.objects.get(id=user_id)
    expiration = now() + timedelta(hours=48)
    record = m.EmailVerification.objects.create(code=uuid.uuid4(), user=user, expiration=expiration)
    record.send_verification_email()
