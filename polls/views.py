from .models import Poll, Guest
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.views.generic.edit import FormView
from .forms import PollCreationForm
from django.shortcuts import redirect
from django.urls import reverse_lazy
from datetime import datetime 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string
from django.conf import settings
from urllib.parse import urlencode
from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import render
from django.contrib import messages
from .tasks import notify_guests_with_changes, invite_guests, send_contact_message


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
       
        success_url = reverse_lazy('polls:poll_detail', kwargs={'guid': poll.guid})
        return redirect(success_url, {'poll': poll})


class PollList(LoginRequiredMixin,  ListView):
    model = Poll
    context_object_name = 'polls'
    template_name='polls/list.html'

    def get_queryset(self):
        current_user = self.request.user
        queryset = Poll.objects.filter(creator=current_user)
        return queryset
    

class PollDetail(DetailView):
    model = Poll
    template_name='polls/show.html'
    context_object_name = 'poll'
    login_url = reverse_lazy('account_login')
    uuid_url_kwarg = 'guid'

    def get_queryset(self):
        current_user = self.request.user
        queryset = Poll.objects.prefetch_related('time_slots')
        if current_user.is_authenticated:
            queryset = queryset.prefetch_related('messages').filter(creator=current_user)
        return queryset
    
    def get(self, request, *args, **kwargs):
        invite = request.GET.get('invite', None)
        gid = request.GET.get('gid', None)

        if not invite and not gid:
            if not request.user.is_authenticated:
                return redirect_to_login(request.get_full_path(), self.login_url)
        
        try:
            poll_guid = self.kwargs[self.uuid_url_kwarg]
            queryset = self.get_queryset()
            poll = queryset.get(guid=poll_guid) if not invite else queryset.get(guid=poll_guid, token=invite)
            return render(request, 'polls/show.html', {'poll': poll})
        except:
            return render(request, '404.html')
        
    
class PollUpdate(LoginRequiredMixin, UpdateView):
    model = Poll
    template_name = "polls/show.html"
    fields = ['event_name', 'event_details', 'event_location', 'rsvp_by']
    uuid_url_kwarg = 'guid'
    
    def get(self, request, *args, **kwargs):
        poll_url = reverse_lazy('polls:poll_detail', kwargs={'guid': self.kwargs[self.uuid_url_kwarg]})
        return redirect(poll_url)

    def post(self, *args, **kwargs):
        post_data = self.request.POST

        if '_method' in post_data and post_data['_method'] == 'put':
            data = {k:v for k,v in post_data.items() if k not in ['csrfmiddlewaretoken', '_method']}
            poll = Poll.objects.get(guid=self.kwargs[self.uuid_url_kwarg])
            
            if 'close' in data:
                poll.rsvp_by = datetime.now().strftime("%Y-%m-%dT%H:%M")
                poll.save()
                if 'notify' in data:
                    notify_guests_with_changes.delay(poll.pk, 'closed')                

            elif 'date' in data:
                poll.time_slots.create(day=data['date'], start=data['start'], end=data['end'])
                
            elif 'timeslots[]' in data:
                timeslots = post_data.getlist('timeslots[]')
                for slot in timeslots:
                    poll.time_slots.get(pk=slot).delete()
                
            else:
                for field, value in data.items():
                    setattr(poll, field, value)
                    poll.save()
                    if field == 'notify':
                        notify_guests_with_changes.delay(poll.pk, 're-opened')                

              
        success_url = reverse_lazy('polls:poll_detail', kwargs={'guid': poll.guid})
        return redirect(success_url, {'poll': poll})
    

class PollDelete(LoginRequiredMixin, DeleteView):
    model = Poll
    success_url = reverse_lazy('polls:my_polls')
    uuid_url_kwarg = 'guid'

    def get_object(self):
        return self.get_queryset().get(guid=self.kwargs[self.uuid_url_kwarg])

    def get(self, request, *args, **kwargs):
        poll_url = reverse_lazy('polls:poll_detail', kwargs={'guid': self.kwargs[self.uuid_url_kwarg]})
        return redirect(poll_url)
    

@login_required
@require_http_methods(['POST'])
def invite(request, guid):
    guests = request.POST.getlist('guest_list[]')

    invite_guests.delay(guid, guests, request.get_host())
    
    return redirect(reverse_lazy('polls:poll_detail', kwargs={'guid': guid}))


@require_http_methods(['POST'])
def add_guest(request, guid=None):
    guest_name = request.POST.get('name')
    guest_email = request.POST.get('email')
    guest_email = guest_email if guest_email else None
    poll = Poll.objects.get(guid=guid)

    try:
        guest = poll.guests.create(name=guest_name, email=guest_email)
        params = {'gid': guest.guid}
        query_string = urlencode(params)
        return redirect(reverse_lazy('polls:poll_detail' , kwargs={'guid': guid}) + 
            '?' + query_string)
    except:
        params = {'invite': poll.token}
        query_string = urlencode(params)
        messages.error(request, 'Name or Email is already exist for another guest')
        return redirect(reverse_lazy('polls:poll_detail' , kwargs={'guid': guid}) + 
            '?' + query_string)
        

@require_http_methods(['GET'])
def get_guest(request, poll_guid=None, guest_guid=None):
    try:
        poll = Poll.objects.get(guid=poll_guid)
        instance = Guest.objects.prefetch_related('votes').get(guid=guest_guid, poll=poll)
        guest = serializers.serialize('json', [instance])
        votes = serializers.serialize('json', instance.votes.all())
        return JsonResponse({'guest': guest, 'votes': votes})
    except:
        return JsonResponse({})
    

@require_http_methods(['POST'])
def edit_guest_name(request, guid=None):
    new_name = request.POST.get('name')
    guest = Guest.objects.select_related('poll').get(guid=guid)

    try:
        guest.name = new_name
        guest.save()
    except:
        messages.error(request, 'This name belongs to another guest. Please, choose a valid name')
    finally:
        params = {'gid': guid}
        query_string = urlencode(params)
        return redirect(reverse_lazy('polls:poll_detail' , kwargs={'guid': guest.poll.guid}) + 
        '?' + query_string)


@require_http_methods(['POST'])
def contact(request):
    data = request.POST
    send_contact_message.delay(data)
    return JsonResponse({'status': 'ok'})