from django.contrib import admin
from support.models import Ticket, Message
from support.services.ticket_admin_service import TicketAdminService


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
        support = obj.support
        username, email = user.username, user.email
        ticket_id = obj.id
        if 'status' in data:
            status = form.cleaned_data['status']
            TicketAdminService.send_mail_change_status(ticket_id, username, support, status, email)

        super().save_model(request, obj, form, change)


admin.site.register(Message)
