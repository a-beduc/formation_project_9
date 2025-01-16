from django.shortcuts import redirect, render
from . import forms, models
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(View, LoginRequiredMixin):
    template_name = 'litrevu/home.html'

    def get(self, request):
        tickets = models.Ticket.objects.all()
        reviews = models.Review.objects.all()
        return render(request, self.template_name, context={'tickets': tickets, 'reviews': reviews})


class TicketCreateView(View, LoginRequiredMixin):
    template_name = 'litrevu/ticket_create.html'
    form_class = forms.TicketForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('home')
        return render(request, self.template_name, context={'form': form})


class TicketUpdateView(View, LoginRequiredMixin):
    template_name = 'litrevu/ticket_update.html'
    form_class = forms.TicketForm

    def get(self, request, ticket_id):
        ticket = models.Ticket.objects.get(pk=ticket_id)
        form = self.form_class(instance=ticket)
        return render(request, self.template_name, context={'form': form, 'ticket': ticket})

    def post(self, request, ticket_id):
        ticket = models.Ticket.objects.get(pk=ticket_id)
        form = self.form_class(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('home')
        return render(request, self.template_name, context={'form': form})


class TicketDeleteView(View, LoginRequiredMixin):
    @staticmethod
    def post(request, ticket_id):
        ticket = models.Ticket.objects.get(pk=ticket_id)
        if ticket.user == request.user:
            ticket.delete()
            return redirect('home')
        return redirect('home')


class ReviewCreateView(View, LoginRequiredMixin):
    template_name = 'litrevu/review_create.html'
    form_class = forms.ReviewForm

    def get(self, request, ticket_id):
        ticket = models.Ticket.objects.get(pk=ticket_id)
        form = self.form_class()
        return render(request, self.template_name, context={'form': form, 'ticket': ticket})

    def post(self, request, ticket_id):
        ticket = models.Ticket.objects.get(id=ticket_id)
        form = self.form_class(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            return redirect('home')
        return render(request, self.template_name, context={'form': form, 'ticket': ticket})


class ReviewUpdateView(View, LoginRequiredMixin):
    template_name = 'litrevu/review_update.html'
    form_class = forms.ReviewForm

    def get(self, request, review_id):
        review = models.Review.objects.get(pk=review_id)
        ticket = models.Ticket.objects.get(pk=review.ticket.id)
        form = self.form_class(instance=review)
        return render(request, self.template_name, context={'form': form, 'ticket': ticket, 'review': review})

    def post(self, request, review_id):
        review = models.Review.objects.get(pk=review_id)
        # not sure if I need to call ticket objet when modifying review, link between ticket and review should
        # already exist, and shouldn't be changed <<< Need to ask s/o
        ticket = models.Ticket.objects.get(pk=review.ticket.id)
        form = self.form_class(request.POST, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            return redirect('home')
        return render(request, self.template_name, context={'form': form, 'ticket': ticket})


class ReviewDeleteView(View, LoginRequiredMixin):
    @staticmethod
    def post(request, review_id):
        review = models.Ticket.objects.get(pk=review_id)
        if review.user == request.user:
            review.delete()
            return redirect('home')
        return redirect('home')


class TicketReviewCreateView(View, LoginRequiredMixin):
    template_name = 'litrevu/ticket_review_create.html'
    ticket_form_class = forms.TicketForm
    review_form_class = forms.ReviewForm

    def get(self, request):
        ticket_form = self.ticket_form_class()
        review_form = self.review_form_class()
        return render(request, self.template_name, context={'ticket_form': ticket_form, 'review_form': review_form})

    def post(self, request):
        ticket_form = self.ticket_form_class(request.POST, request.FILES)
        review_form = self.review_form_class(request.POST)
        if ticket_form.is_valid() and review_form.is_valid():

            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()

            return redirect('home')
        return render(request, self.template_name, context={'ticket_form': ticket_form, 'review_form': review_form})
