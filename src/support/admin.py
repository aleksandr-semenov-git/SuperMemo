from django.contrib import admin
from support.models import Ticket, Message
from django.core.mail import send_mail


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
            send_mail(subject=f'Status of your ticket №{ticket_id} was changed. ',
                      message=f'Hello, dear {username}. '
                              f'We want you to know that {support} have changed status of your ticket to {status}. '
                              f'Best regards, CEO of GlobeMemo inc. Aleksandr Semenov. ',
                      from_email=None,
                      recipient_list=[email])

        super().save_model(request, obj, form, change)


admin.site.register(Message)
