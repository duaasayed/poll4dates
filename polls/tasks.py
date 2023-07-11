from django.core.mail import send_mail
from celery import shared_task
from django.conf import settings
from .models import Poll

@shared_task
def fetch_result_and_send_email(pk):
    poll = Poll.objects.get(pk=pk)
    result = fetch_result(poll)
    send_email(poll, result)

def fetch_result(poll):
    chosen_timeslots = []
    max_vote = poll.max_vote

    for timeslot in poll.time_slots.all():
        if timeslot.votes_count == max_vote:
            formatted_timeslot = format_timeslot(timeslot)
            chosen_timeslots.append(formatted_timeslot)
    return chosen_timeslots


def format_timeslot(timeslot):
    return f'{timeslot.day} @ {timeslot.start} - {timeslot.end}'


def send_email(poll, result):
    subject = 'Poll Result'
    message = 'Most of yout guests have chosen '

    if len(result) == 1:
        message += f'this time slot {result[0]} as suitable for them'

    else:
        for timeslot in result:
            message += timeslot + ', '
        message = message[:-2] + ' as suitable for them'

    recipient_list = fetch_recipients_emails(poll)
    send_mail(subject=subject, message=message, from_email=settings.EMAIL_HOST_USER, recipient_list=recipient_list)


def fetch_recipients_emails(poll):
    recipient_list = [poll.creator.email]

    for guest in poll.guests.all():
        if guest.email:
            recipient_list.append(guest.email)

    return recipient_list