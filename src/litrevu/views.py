from django.shortcuts import redirect, render
from . import forms, models
from myauth.models import User
from django.db.models import Q
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from itertools import chain
from django.contrib import messages
from django.core.paginator import Paginator


class HomeView(LoginRequiredMixin, View):
    """
    Display a feed of both Tickets and Reviews relevant to the logged-in
    user.
    The feed includes:
        + The user own posts,
        + Posts created by user they follow,
        + Reviews of tickets that the user created,
        + Reviews of tickets created by followed users.
    Additionally, reviews from blocked users are flagged as blocked.
    """
    template_name = 'litrevu/home.html'

    def get(self, request):
        """
        Handle GET requests.

        :param request: An HttpRequest object.
        :return: An HttpResponse object with paginated posts.
        """
        followed = (
            models.UserFollow.objects.filter(user=request.user).
            values_list('followed_user')
        )
        excluded = (
            models.UserBlock.objects.filter(user=request.user).
            values_list('blocked_user', flat=True)
        )
        reviews = (
            models.Review.objects.filter(
                Q(user=request.user) |
                Q(user__in=followed) |
                Q(ticket__user=request.user) |
                Q(ticket__user__in=followed)
            )
        )
        for review in reviews:
            if review.user.id in excluded:
                review.blocked = True
        tickets = (
            models.Ticket.objects.filter(
                Q(user=request.user) |
                Q(user__in=followed)
            )
        )
        for ticket in tickets:
            # user_has_reviewed is used in the litrevu/ticket_snippet.html
            # template to show/hide the "Créer une critique" button
            ticket.user_has_reviewed = (
                ticket.review_set.filter(user=request.user).exists()
            )
        posts = (
            sorted(
                chain(reviews, tickets),
                key=lambda post: post.time_created,
                reverse=True
            )
        )
        paginator = Paginator(posts, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'page_obj': page_obj}
        return render(request, self.template_name, context=context)


class TicketCreateView(LoginRequiredMixin, View):
    """
    View for creating a new Ticket.
    """
    template_name = 'litrevu/ticket_create.html'
    form_class = forms.TicketForm

    def get(self, request):
        """
        Handle GET requests.

        :param request: An HttpRequest object.
        :return: An HttpResponse object with a blank ticket form.
        """
        form = self.form_class()
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        """
        Handle POST requests. Validate and create a new Ticket.
        If valid, redirects to the home page; otherwise, displays the
        form.

        :param request: An HttpRequest object containing form data.
        :return: An HttpResponse redirect to 'home' on success or
        re-renders form on invalid submission.
        """
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('home')
        return render(request, self.template_name, context={'form': form})


class TicketUpdateView(LoginRequiredMixin, View):
    """
    View for updating a ticket. Users can only update their own tickets.
    """
    template_name = 'litrevu/ticket_update.html'
    form_class = forms.TicketForm

    def get(self, request, ticket_id):
        """
        Handle GET requests. Render the update form for the specified
        ticket.

        :param request: an HttpRequest object.
        :param ticket_id: The primary key (id) of the ticket to update.
        :return: HttpResponse with a populated TicketForm.
        """
        ticket = models.Ticket.objects.get(id=ticket_id)
        form = self.form_class(instance=ticket)
        return render(request, self.template_name,
                      context={'form': form, 'ticket': ticket})

    def post(self, request, ticket_id):
        """
        Handle POST requests.
        Validate and update a ticket. If valid, redirects to the home
        page; otherwise, re-displays the form.

        :param request: An HttpRequest object containing form data.
        :param ticket_id: The primary key (id) of the ticket being
        updated.
        :return: An HttpResponse redirect to the previous page on
        success or re-renders form on invalid submission.
        """
        ticket = models.Ticket.objects.get(id=ticket_id)
        form = (
            self.form_class(request.POST, request.FILES, instance=ticket)
        )
        if form.is_valid():
            form.save()
            return redirect('home')
        return render(request, self.template_name, context={'form': form})


class TicketDeleteView(LoginRequiredMixin, View):
    """
    View to handle deletion of a user's ticket.
    """

    def post(self, request, ticket_id):
        """
        Handle POST requests. Delete the specified ticket.

        :param request: An HttpsRequest object.
        :param ticket_id: The primary key (id) of the ticket being
        deleted.
        :return: HttpResponse redirect to the previous page
        """
        ticket = models.Ticket.objects.get(id=ticket_id)
        if ticket.user == request.user:
            ticket.delete()
        # Redirect to the previous page or fallback to 'home'
        return redirect(self.request.META.get('HTTP_REFERER', 'home'))


class ReviewCreateView(LoginRequiredMixin, View):
    """
    View for creating a new review of an existing Ticket.
    """
    template_name = 'litrevu/review_create.html'
    form_class = forms.ReviewForm

    def get(self, request, ticket_id):
        """
        Handle GET requests. Render the review form for the specified
        ticket.
        :param request: an HttpRequest object.
        :param ticket_id: The primary key (id) of the ticket to review.
        :return: HttpResponse with a blank Review Form.
        """
        ticket = models.Ticket.objects.get(id=ticket_id)
        ticket.user_has_reviewed = ticket.review_set.filter(
            user=request.user
        ).exists()
        form = self.form_class()
        return render(request, self.template_name,
                      context={'form': form, 'ticket': ticket})

    def post(self, request, ticket_id):
        """
        Handle POST requests. Validate and create a new review.
        :param request: an HttpRequest object.
        :param ticket_id: The primary key (id) of the ticket to review.
        :return: HttpResponse redirect to 'home' or re-render a
        populated Review Form on invalid submission.
        """
        ticket = models.Ticket.objects.get(id=ticket_id)
        ticket.user_has_reviewed = (
            ticket.review_set.filter(user=request.user).exists())
        form = self.form_class(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            return redirect('home')
        return render(request, self.template_name,
                      context={'form': form, 'ticket': ticket})


class ReviewUpdateView(LoginRequiredMixin, View):
    """
    View for updating a review of an existing Review.
    """
    template_name = 'litrevu/review_update.html'
    form_class = forms.ReviewForm

    def get(self, request, review_id):
        """
        Handle GET requests. Render the review form for the specified
        review.
        :param request: an HttpRequest object.
        :param review_id: The primary key (id) of the review to update.
        :return: HttpResponse with a populated Review Form
        """
        review = models.Review.objects.get(id=review_id)
        ticket = models.Ticket.objects.get(id=review.ticket.id)
        ticket.user_has_reviewed = (
            ticket.review_set.filter(user=request.user).exists())
        form = self.form_class(instance=review)
        return render(request, self.template_name,
                      context={'form': form,
                               'ticket': ticket,
                               'review': review})

    def post(self, request, review_id):
        """
        Handle POST requests. Save changes to the specified review if
        valid.
        :param request: an HttpRequest object.
        :param review_id: The primary key (id) of the review to update.
        :return: HttpRespons redirect to 'home' or re-render a
        populated Review Form on invalid submission.
        """
        review = models.Review.objects.get(id=review_id)
        ticket = models.Ticket.objects.get(id=review.ticket.id)
        ticket.user_has_reviewed = (
            ticket.review_set.filter(user=request.user).exists())
        form = self.form_class(request.POST, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.save()
            return redirect('home')
        return render(request, self.template_name,
                      context={'form': form, 'ticket': ticket})


class ReviewDeleteView(LoginRequiredMixin, View):
    """
    View handling the deletion of a user's review.
    """

    def post(self, request, review_id):
        """
        Handle POST requests. Redirect to the previous page on deletion.
        :param request: An HttpRequest object.
        :param review_id: The primary key (id) of the review to delete.
        :return: HttpResponse redirect to the previous page
        """
        review = models.Review.objects.get(id=review_id)

        if review.user == request.user:
            review.delete()
        # Redirect to the previous page or fallback to 'home'
        return redirect(self.request.META.get('HTTP_REFERER', 'home'))


class TicketReviewCreateView(LoginRequiredMixin, View):
    """
    View that allows users to create both a ticket and a review at the
    same time.
    """
    template_name = 'litrevu/ticket_review_create.html'
    ticket_form_class = forms.TicketForm
    review_form_class = forms.ReviewForm

    def get(self, request):
        """
        Handle GET requests, render blanks ticket form and review form.
        :param request: an HttpRequest object.
        :return: HttpResponse with two empty forms: TicketForm and
        ReviewForm.
        """
        ticket_form = self.ticket_form_class()
        review_form = self.review_form_class()
        return render(request, self.template_name,
                      context={'ticket_form': ticket_form,
                               'review_form': review_form})

    def post(self, request):
        """
        Handle POST requests. Validate and create both the Ticket and
        its associated Review.
        :param request: An HttpRequest object containing form data for
        both ticket and review.
        :return: An HttpResponse redirect to 'home' or re-render a
        populated Ticket Form and Review Form on invalid submission of
        any of them.
        """
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
        return render(request, self.template_name,
                      context={
                          'ticket_form': ticket_form,
                          'review_form': review_form})


class BaseRelationView(LoginRequiredMixin, View):
    """
    Basic view for creating Follower/Followed and Blocker/Blocked
    relations for the 'litrevu/subscription.html' template.
    """
    template_name = 'litrevu/subscription.html'
    form_class_follow = forms.UserFollowForm
    form_class_block = forms.UserBlockForm

    def get_context_data(self, request, follow_form=None, block_form=None):
        """
        Get the context for the subscription template, if not specified
        send empty follow and block forms
        :param request: An HttpRequest object.
        :param follow_form: An instance of forms.UserFollowsForm.
        :param block_form: An instance of forms.UserBlocksForm.
        :return: A dictionary of context variables.
        """
        followed = (
            models.UserFollow.objects.filter(user=request.user).
            select_related('followed_user'))
        following = (
            models.UserFollow.objects.filter(followed_user=request.user).
            select_related('user'))
        blocked = (
            models.UserBlock.objects.filter(user=request.user).
            select_related('blocked_user'))
        if not follow_form:
            follow_form = self.form_class_follow()
        if not block_form:
            block_form = self.form_class_block()
        return {
            'followed': followed,
            'following': following,
            'blocked': blocked,
            'follow_form': follow_form,
            'block_form': block_form
        }

    def get(self, request):
        """
        Handle GET requests. Render the subscription page, displaying
        the user's follow and block relationships.
        :param request: An HttpRequest object.
        :return: HttpResponse with follow/block relations and forms for
        following and blocking users.
        """
        context = self.get_context_data(request)
        return render(request, self.template_name, context=context)

    def handle_relation(self, request, username):
        raise NotImplementedError(
            "handle_relation must be implemented in subclass")


class FollowView(BaseRelationView):
    """
    View for creating a relation of follower/followed between two users
    """
    def post(self, request):
        """
        Handle POST requests. Follow the specified user.
        :param request: An HttpRequest object.
        :return: HttpResponse redirect to 'litrevu/subscription.html'
        template
        """
        follow_form = self.form_class_follow(request.POST)
        if follow_form.is_valid():
            username_to_follow = follow_form.cleaned_data['username']
            self.handle_relation(request, username_to_follow)

        context = self.get_context_data(request, follow_form=follow_form)
        return render(request, self.template_name, context=context)

    def handle_relation(self, request, username_to_follow):
        """
        Verify several conditions before creating a follower/followed
        relation between two users. Display error messages when the
        criteria are not met.
        """
        try:
            user_to_follow = User.objects.get(username=username_to_follow)
            already_followed = (
                models.UserFollow.objects.
                filter(user=request.user, followed_user=user_to_follow))
            blocked_by_user = (
                models.UserBlock.objects.
                filter(user=request.user, blocked_user=user_to_follow))
            blocked_by_user_to_follow = (
                models.UserBlock.objects.
                filter(user=user_to_follow, blocked_user=request.user))

            # verify several conditions before creating the follow
            # relationship
            if already_followed.exists():
                messages.error(
                    request,
                    message=f"Vous êtes déjà abonné à {username_to_follow}.",
                    extra_tags="follow_message")
            elif (blocked_by_user.exists() or
                  blocked_by_user_to_follow.exists()):
                messages.error(
                    request,
                    message=f"Impossible de suivre {username_to_follow}.",
                    extra_tags="follow_message")
            elif request.user.id == user_to_follow.id:
                messages.error(
                    request,
                    message="Vous ne pouvez pas vous suivre vous-même.",
                    extra_tags="follow_message")
            else:
                new_follow = models.UserFollow.objects.create(
                    user=request.user,
                    followed_user=user_to_follow)
                new_follow.save()

        except User.DoesNotExist:
            messages.error(
                request,
                message=f"L'utilisateur '{username_to_follow}' n'existe pas.",
                extra_tags='follow_message')


class BlockView(BaseRelationView):
    """
    View for creating a relation of blocker/blocked between two users
    """
    def post(self, request):
        """
        Handle POST requests. Block the specified user.
        :param request: An HttpRequest object.
        :return: HttpResponse redirect to 'litrevu/subscription.html' template
        """
        block_form = self.form_class_block(request.POST)
        if block_form.is_valid():
            username_to_block = block_form.cleaned_data['username']
            self.handle_relation(request, username_to_block)

        context = self.get_context_data(request, block_form=block_form)
        return render(request, self.template_name, context=context)

    def handle_relation(self, request, username_to_block):
        """
        Verify several conditions before creating a blocker/blocked
        relation between two users. Display error messages when the
        criteria are not met.
        """
        try:
            user_to_block = User.objects.get(username=username_to_block)
            already_blocked = models.UserBlock.objects.filter(
                user=request.user, blocked_user=user_to_block)
            if already_blocked.exists():
                messages.error(
                    request,
                    message=f"Vous avez déjà bloqué {username_to_block}.",
                    extra_tags="block_message")
            elif request.user.id == user_to_block.id:
                messages.error(
                    request,
                    message="Vous ne pouvez pas vous bloquer vous-même",
                    extra_tags="block_message")
            else:
                block = (
                    models.UserBlock.objects.create(
                        user=request.user,
                        blocked_user=user_to_block))
                followed_by_user = (
                    models.UserFollow.objects.filter(
                        user=request.user,
                        followed_user=user_to_block))
                if followed_by_user.exists():
                    followed_by_user.delete()
                followed_by_user_to_block = (
                    models.UserFollow.objects.filter(
                        user=user_to_block,
                        followed_user=request.user))
                if followed_by_user_to_block.exists():
                    followed_by_user_to_block.delete()

                block.save()

        except User.DoesNotExist:
            messages.error(
                request,
                message=f"L'utilisateur '{username_to_block}' n'existe pas.",
                extra_tags='block_message')


class BaseDeleteView(LoginRequiredMixin, View):
    """
    Basic view for deleting Follower/Followed and Blocker/Blocked
    relations refresh page after being called.
    """
    def post(self, request, relation_id):
        """
        Handle POST requests. Delete follower/followed or blocker
        relation.
        :param request: An HttpRequest object.
        :param relation_id: The id of the relation to delete.
        :return: HttpResponse refresh the current page
        """
        selected_relation = self.get_relation_from_id(relation_id)
        if selected_relation.user == request.user:
            selected_relation.delete()
        return redirect(self.request.META.get("HTTP_REFERER"))

    def get_relation_from_id(self, relation_id):
        raise NotImplementedError(
            "get_relation_from_id must be implemented in subclass")


class FollowDeleteView(BaseDeleteView):
    """
    View for deleting Follower/Followed relations refresh page after
    being called.
    """
    def get_relation_from_id(self, relation_id):
        return models.UserFollow.objects.get(id=relation_id)


class BlockDeleteView(BaseDeleteView):
    """
    View for deleting Follower/Followed relations refresh page after
    being called.
    """
    def get_relation_from_id(self, relation_id):
        return models.UserBlock.objects.get(id=relation_id)


class PostsView(LoginRequiredMixin, View):
    """
    View for displaying all posts made by the user.
    """
    template_name = 'litrevu/posts.html'

    def get(self, request):
        """
        Handle GET requests. Display all posts made by the user.
        :param request: An HttpRequest object.
        :return: HttpResponse redirect to 'litrevu/posts.html' template
        """
        reviews = models.Review.objects.filter(user=request.user)
        tickets = models.Ticket.objects.filter(user=request.user)
        for ticket in tickets:
            ticket.user_has_reviewed = (
                ticket.review_set.filter(user=request.user).exists())
        posts = (
            sorted(chain(reviews, tickets),
                   key=lambda post: post.time_created,
                   reverse=True))

        paginator = Paginator(posts, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'page_obj': page_obj}

        return render(request, self.template_name, context=context)
