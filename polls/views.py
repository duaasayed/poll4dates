from .models import Poll
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.views.generic.edit import FormView
from .forms import PollCreationForm
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string
from django.conf import settings

class PollCreate(FormView):
    template_name = 'polls/create.html'
    form_class = PollCreationForm
    login_url = reverse_lazy('account_login')
    
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            request.session['form_data'] = request.POST
            request.session['timeslots'] = request.POST.getlist('timeslots')
            return redirect_to_login(self.request.get_full_path(), self.login_url)
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        poll = form.save()
        poll.creator = self.request.user
        poll.save()
        for slot in form.cleaned_data['timeslots']:
            poll.time_slots.create(**slot)
        
        if 'form_data' in self.request.session: 
            del self.request.session['form_data']
            del self.request.session['timeslots']
       
        success_url = reverse_lazy('polls:poll_detail', kwargs={'pk': poll.pk})
        return redirect(success_url, {'poll': poll})


class PollList(LoginRequiredMixin,  ListView):
    model = Poll
    context_object_name = 'polls'
    template_name='polls/list.html'

    def get_queryset(self):
        current_user = self.request.user
        queryset = Poll.objects.filter(creator=current_user)
        return queryset
    

class PollDetail(LoginRequiredMixin, DetailView):
    model = Poll
    template_name='polls/show.html'
    context_object_name = 'poll'

    def get_queryset(self):
        current_user = self.request.user
        queryset = Poll.objects.prefetch_related('time_slots').filter(creator=current_user)
        return queryset
        
    
class PollUpdate(LoginRequiredMixin, UpdateView):
    model = Poll
    template_name = "polls/show.html"
    fields = ['event_name', 'event_details', 'event_location', 'rsvp_by']
    
    def get(self, request, *args, **kwargs):
        poll_url = reverse_lazy('polls:poll_detail', kwargs={'pk': self.kwargs[self.pk_url_kwarg]})
        return redirect(poll_url)

    def post(self, *args, **kwargs):
        post_data = self.request.POST

        if '_method' in post_data and post_data['_method'] == 'put':
            data = {k:v for k,v in post_data.items() if k not in ['csrfmiddlewaretoken', '_method']}
            
            poll = Poll.objects.get(pk=self.get_object().pk)
            
            for field, value in data.items():
                setattr(poll, field, value)
                poll.save()

            if 'close' in data:
                data['rsvp_by'] = timezone.now()
            
            if 'date' in data:
                poll.time_slots.create(day=data['date'], start=data['start'], end=data['end'])

            if 'timeslots[]' in data:
                timeslots = post_data.getlist('timeslots[]')
                for slot in timeslots:
                    poll.time_slots.get(pk=slot).delete()
              
        success_url = reverse_lazy('polls:poll_detail', kwargs={'pk': poll.pk})
        return redirect(success_url, {'poll': poll})
    

class PollDelete(LoginRequiredMixin, DeleteView):
    model = Poll
    success_url = reverse_lazy('polls:my_polls')

    def get(self, request, *args, **kwargs):
        poll_url = reverse_lazy('polls:poll_detail', kwargs={'pk': self.kwargs[self.pk_url_kwarg]})
        return redirect(poll_url)
    

@login_required
@require_http_methods(['POST'])
def invite(request, pk):
    poll = Poll.objects.get(pk=pk)
    guests = request.POST.getlist('guest_list[]')

    mails = []

    for guest in guests:
        guest_info = guest.split(' ')

        name = ' '.join(guest_info[:-1])
        email = guest_info[-1]
        
        poll.guests.create(name=name, email=email)

        mail_body = render_to_string('emails/invite.html', {'poll': poll, 'guest': name})
        mail = EmailMultiAlternatives('You got an invitation', mail_body, settings.EMAIL_HOST_USER, [email])
        mail.attach_alternative(mail_body, 'text/html')
        mails.append(mail)
    
    connection = get_connection()
    connection.send_messages(mails)
    
    return redirect(reverse_lazy('polls:poll_detail', kwargs={'pk': pk}))


def vote(request, token):
    poll = Poll.objects.get(token=token)
    return redirect(reverse_lazy('polls:poll_detail', kwargs={'pk': poll.pk}))