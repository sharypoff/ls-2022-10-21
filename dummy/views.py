from django.http import HttpResponse, Http404
from django.template import loader
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.views.generic.edit import CreateView
from django.urls import reverse
from .models import SimpleLamp, Ticket, PassangerInfo


def index(request):
    context = {}
    return render(request, 'dummy/index.html', context)


def simplelamp_details(request, lamp_id):
    lamp = get_object_or_404(SimpleLamp, pk=lamp_id)

    return render(request, 'dummy/simplelamp_details.html', {'lamp': lamp})


def simplelamp_list(request):
    lamps = SimpleLamp.objects.all()

    return render(request, 'dummy/simplelamp_list.html', {'lamps': lamps})


class LampList(generic.ListView):
    template_name = 'dummy/simplelamp_list.html'
    context_object_name = 'lamps'

    def get_queryset(self):
        return SimpleLamp.objects.order_by('address')


class LampDetails(generic.DetailView):
    template_name = 'dummy/simplelamp_details.html'
    context_object_name = 'lamp'
    model = SimpleLamp


class LampCreateView(CreateView):
    fields = ['address', 'lamp_type']
    model = SimpleLamp

    def get_success_url(self):
        return reverse('simplelamp_detail', kwargs={'pk': self.object.pk})


class ValadationError(Exception):
    def __init__(self, error):
        self.error = error


def book_ticket(request, pk=None):
    ticket = get_object_or_404(Ticket, pk=pk)
    try:
        passanger_count = int(request.GET["pcnt"])
    except (KeyError, ValueError):
        raise Http404
    context = {
        "ticket": ticket,
        "passanger_count": passanger_count,
        "passanger_range": range(1, passanger_count + 1),
    }

    if request.method == 'POST':
        try:
            if ticket.passangerinfo_set.exists():
                raise ValadationError(error="Билет продан")
            passengers = []
            i = 1
            while True:
                firstname = request.POST.get(f'firstname-{i}')

                if firstname is not None:
                    if not firstname or len(firstname) > 100:
                        raise ValadationError(error="Ошибка заполнения формы")
                    passengers.append(
                        {
                            "firstname": firstname,
                        }
                    )
                else:
                    break
                i += 1

            for passenger in passengers:
                PassangerInfo.objects.create(
                    firstname=passenger["firstname"],
                    ticket=ticket,
                )
            # ticket.passangerinfo_set.create(firstname=firstname)
            redirect(reverse('book_ticket', kwargs={"pk": ticket.id}))
        except ValadationError as exc:
            context["error"] = exc.error

    return render(request, 'dummy/book_ticket.html', context)


