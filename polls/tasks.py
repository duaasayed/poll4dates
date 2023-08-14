from django.core.mail import send_mail
from celery import shared_task
from django.conf import settings
from .models import Poll
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string

@shared_task
def fetch_result_and_send_email(pk):
    poll = Poll.objects.get(pk=pk)

    result = fetch_result(poll)

    subject = 'Poll Result'
    message = 'Most of yout guests have chosen '

    if len(result) == 1:
        message += f'this time slot {result[0]} as suitable for them'

    else:
        for timeslot in result:
            message += timeslot + ', '
        message = message[:-2] + ' as suitable for them'

    recipient_list = fetch_recipients_emails(poll)
    send_email(subject, message, recipient_list)


@shared_task
def notify_guests_with_changes(pk, event):
    poll = Poll.objects.get(pk=pk)
    recipient_list = fetch_recipients_emails(poll)
    subject = f'The poll for "{poll.event_name}" event has been {event}'
    message = f'The poll for "{poll.event_name}" event has been {event}. You can visit the poll page and check the result'
    send_email(subject, message, recipient_list)


@shared_task
def invite_guests(pk, guests, host):
    poll = Poll.objects.get(pk=pk)

    mails = []

    for guest in guests:
        guest_info = guest.split(' ')

        name = ' '.join(guest_info[:-1])
        email = guest_info[-1]
        
        try: 
            guest = poll.guests.create(name=name, email=email)
            mail_body = render_to_string('emails/invite.html', {'poll': poll, 'guest': guest, 'host': host})
            mail = EmailMultiAlternatives('You got an invitation', mail_body, settings.EMAIL_HOST_USER, [email])
            mail.attach_alternative(mail_body, 'text/html')
            mails.append(mail)
            connection = get_connection()
            connection.send_messages(mails)
        except Exception as e:
            pass
    
    



@shared_task
def send_contact_message(data):
    mail_body = render_to_string('emails/contact.html', {'data': data})
    mail = EmailMultiAlternatives(
        'You got a new message from your website',
        mail_body,
        settings.EMAIL_HOST_USER,
        (settings.ADMIN_EMAIL,),
        reply_to=(data['email'],)
    )
    mail.attach_alternative(mail_body, 'text/html')
    mail.send()


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


def send_email(subject, message, recipient_list):
    send_mail(subject=subject, message=message, 
              from_email=settings.EMAIL_HOST_USER, 
              recipient_list=recipient_list)


def fetch_recipients_emails(poll):
    recipient_list = [poll.creator.email]

    for guest in poll.guests.all():
        if guest.email:
            recipient_list.append(guest.email)

    return recipient_list