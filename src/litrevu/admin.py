from django.contrib import admin
from litrevu.models import Ticket, Review, UserFollow, UserBlock


class AdminUtilsMixin:
    @staticmethod
    def short_text(text, max_length=50):
        if text:
            return text[:max_length] + (
                '...' if len(text) > max_length else ''
            )
        return ''

    @staticmethod
    def format_datetime(date_obj):
        if date_obj:
            return date_obj.strftime('%Y-%m-%d')
        return ''


@admin.register(Ticket)
class TicketAdmin(AdminUtilsMixin, admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'date_created',
                    'snippet_description')
    search_fields = ('title', 'user__username')

    def snippet_description(self, obj):
        return self.short_text(obj.description)

    def date_created(self, obj):
        return self.format_datetime(obj.time_created)


@admin.register(Review)
class ReviewAdmin(AdminUtilsMixin, admin.ModelAdmin):
    list_display = ('id', 'ticket__title', 'user', 'headline', 'rating',
                    'date_created', 'short_body')
    search_fields = ('ticket__title', 'user__username')

    def short_body(self, obj):
        return self.short_text(obj.body)

    def date_created(self, obj):
        return self.format_datetime(obj.time_created)


@admin.register(UserFollow)
class UserFollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'followed_user')
    search_fields = ('user', 'followed_user')


@admin.register(UserBlock)
class UserBlockAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'blocked_user')
    search_fields = ('user', 'blocked_user')
