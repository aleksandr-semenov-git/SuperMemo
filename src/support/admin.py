from django.contrib import admin
from support.models import Ticket, Message
from src.tasks import celery_send_email_change_status


class MessageInline(admin.TabularInline):
    model = Message
    extra = 1


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('status', 'issue', 'description', 'support')
    list_filter = ('status', 'support__groups')
    search_fields = ('created_at', 'edited_at', )
    inlines = [MessageInline]
    save_on_top = True
    fieldsets = (
        (None, {
            "fields": (('user', 'support', 'status', 'issue'), )
        }),
        (None, {
            "fields": ('description',)
        })
    )

    def save_model(self, request, obj, form, change):
        data = form.changed_data
        user = obj.user
        support_name = obj.support.username
        username, email = user.username, user.email
        ticket_id = obj.id

        if 'status' in data:
            status = form.cleaned_data['status']
            celery_send_email_change_status.delay(ticket_id, username, support_name, status, email)

        super().save_model(request, obj, form, change)


admin.site.register(Message)
