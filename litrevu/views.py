from django.shortcuts import redirect, render
from . import forms, models
from myauth.models import User
from django.db.models import CharField, Value, Q
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from itertools import chain


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
        ticket = models.Ticket.objects.get(id=ticket_id)
        form = self.form_class(instance=ticket)
        return render(request, self.template_name, context={'form': form, 'ticket': ticket})

    def post(self, request, ticket_id):
        ticket = models.Ticket.objects.get(id=ticket_id)
        form = self.form_class(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('home')
        return render(request, self.template_name, context={'form': form})


class TicketDeleteView(View, LoginRequiredMixin):

    def post(self, request, ticket_id):
        ticket = models.Ticket.objects.get(id=ticket_id)
        if ticket.user == request.user:
            ticket.delete()
            return redirect('home')
        return redirect('home')


class ReviewCreateView(View, LoginRequiredMixin):
    template_name = 'litrevu/review_create.html'
    form_class = forms.ReviewForm

    def get(self, request, ticket_id):
        ticket = models.Ticket.objects.get(id=ticket_id)
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
        review = models.Review.objects.get(id=review_id)
        ticket = models.Ticket.objects.get(id=review.ticket.id)
        form = self.form_class(instance=review)
        return render(request, self.template_name, context={'form': form, 'ticket': ticket, 'review': review})

    def post(self, request, review_id):
        review = models.Review.objects.get(id=review_id)
        ticket = models.Ticket.objects.get(id=review.ticket.id)
        form = self.form_class(request.POST, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.save()
            return redirect('home')
        return render(request, self.template_name, context={'form': form, 'ticket': ticket})


class ReviewDeleteView(View, LoginRequiredMixin):
    def post(self, request, review_id):
        review = models.Review.objects.get(id=review_id)

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


class UserFollowsView(View, LoginRequiredMixin):
    template_name = 'litrevu/subscription.html'
    form_class = forms.UserFollowsForm

    def get(self, request):
        followed = models.UserFollows.objects.filter(user=request.user).select_related('followed_user')
        following = models.UserFollows.objects.filter(followed_user=request.user).select_related('user')
        blocked = models.UserBlocks.objects.filter(user=request.user).select_related('blocked_user')

        block_form = forms.UserBlocksForm()

        follow_form = self.form_class()
        return render(request, self.template_name,
                      context={'followed': followed, 'following': following, 'follow_form': follow_form,
                               'blocked': blocked, 'block_form': block_form}
                      )

    def post(self, request):
        followed = models.UserFollows.objects.filter(user=request.user).select_related('followed_user')
        following = models.UserFollows.objects.filter(followed_user=request.user).select_related('user')
        blocked = models.UserBlocks.objects.filter(user=request.user).select_related('blocked_user')

        block_form = forms.UserBlocksForm()

        follow_form = self.form_class(request.POST)
        if follow_form.is_valid():
            username_to_follow = follow_form.cleaned_data['username']

            try:
                user_to_follow = User.objects.get(username=username_to_follow)
                already_followed = models.UserFollows.objects.filter(
                    user=request.user, followed_user=user_to_follow)

                blocked_by_user = models.UserBlocks.objects.filter(
                    user=request.user, blocked_user=user_to_follow
                )

                blocked_by_user_to_follow = models.UserBlocks.objects.filter(
                    user=user_to_follow, blocked_user=request.user
                )

                if (not blocked_by_user.exists() and
                        not blocked_by_user_to_follow.exists() and
                        not already_followed.exists() and
                        request.user.id != user_to_follow.id):
                    new_follow = models.UserFollows.objects.create(user=request.user, followed_user=user_to_follow)
                    new_follow.save()

            except User.DoesNotExist:
                pass

        return render(request, self.template_name,
                      context={'followed': followed, 'following': following, 'follow_form': follow_form,
                               'blocked': blocked, 'block_form': block_form}
                      )


class UserFollowsDeleteView(View, LoginRequiredMixin):
    def post(self, request, user_followed_relation_id):
        followed = models.UserFollows.objects.get(id=user_followed_relation_id)
        if followed.user == request.user:
            followed.delete()
        return redirect('subscription_follow')


# this view is never called, might be good to delete it.
class UserBlocksView(View, LoginRequiredMixin):
    template_name = 'litrevu/subscription.html'
    form_class = forms.UserBlocksForm

    def get(self, request):
        followed = models.UserFollows.objects.filter(user=request.user).select_related('followed_user')
        following = models.UserFollows.objects.filter(followed_user=request.user).select_related('user')
        blocked = models.UserBlocks.objects.filter(user=request.user).select_related('blocked_user')

        follow_form = forms.UserFollowsForm()
        block_form = self.form_class()

        return render(request, self.template_name,
                      context={'followed': followed, 'following': following, 'blocked': blocked,
                               'follow_form': follow_form, 'block_form': block_form}
                      )

    def post(self, request):
        followed = models.UserFollows.objects.filter(user=request.user).select_related('followed_user')
        following = models.UserFollows.objects.filter(followed_user=request.user).select_related('user')
        blocked = models.UserBlocks.objects.filter(user=request.user).select_related('blocked_user')

        follow_form = forms.UserFollowsForm()

        block_form = self.form_class(request.POST)
        if block_form.is_valid():
            username_to_block = block_form.cleaned_data['username']

            try:
                user_to_block = User.objects.get(username=username_to_block)
                already_blocked = models.UserBlocks.objects.filter(
                    user=request.user, blocked_user=user_to_block)
                if not already_blocked.exists() and request.user.id != user_to_block.id:
                    block = models.UserBlocks.objects.create(user=request.user, blocked_user=user_to_block)

                    followed_by_user = models.UserFollows.objects.filter(
                        user=request.user, followed_user=user_to_block)
                    if followed_by_user.exists():
                        followed_by_user.delete()

                    followed_by_user_to_block = models.UserFollows.objects.filter(
                        user=user_to_block, followed_user=request.user)
                    if followed_by_user_to_block.exists():
                        followed_by_user_to_block.delete()

                    block.save()

            except User.DoesNotExist:
                pass

        return render(request, self.template_name,
                      context={'followed': followed, 'following': following, 'blocked': blocked,
                               'follow_form': follow_form, 'block_form': block_form})


class UserBlocksDeleteView(View, LoginRequiredMixin):
    def post(self, request, user_blocked_relation_id):
        blocked = models.UserBlocks.objects.get(id=user_blocked_relation_id)
        if blocked.user == request.user:
            blocked.delete()
        return redirect('subscription_follow')


class PostsView(View, LoginRequiredMixin):
    template_name = 'litrevu/posts.html'

    def get(self, request):
        reviews = models.Review.objects.filter(user=request.user)
        reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
        tickets = models.Ticket.objects.filter(user=request.user)
        tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
        posts = sorted(chain(reviews, tickets), key=lambda post: post.time_created, reverse=True)
        return render(request, self.template_name, context={'posts': posts})
