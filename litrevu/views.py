from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from . import forms, models


@login_required
def home(request):
    tickets = models.Ticket.objects.all()
    return render(request, 'litrevu/home.html', context={'tickets': tickets})


@login_required
def ticket_upload(request):
    form = forms.TicketForm()
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        ticket = form.save(commit=False)
        ticket.user = request.user
        ticket.save()
        return redirect('home')
    return render(request, 'litrevu/ticket_upload.html', context={'form': form})


@login_required
def ticket_edit(request, ticket_id):
    ticket = models.Ticket.objects.get(id=ticket_id)

    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('home')

    else:
        form = forms.TicketForm(instance=ticket)

    return render(request, 'litrevu/ticket_edit.html', context={'form': form})


@login_required
def review_upload(request, ticket_id):
    ticket = models.Ticket.objects.get(id=ticket_id)

    if request.method == 'POST':
        form = forms.ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            return redirect('home')
    else:
        form = forms.ReviewForm()

    return render(request, 'litrevu/review_upload.html', context={'form': form, 'ticket': ticket})
