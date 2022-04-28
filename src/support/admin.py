from django.contrib import admin
from support.models import Ticket, Message
from django.core.mail import send_mail


class MessageInline(admin.TabularInline):
    model = Message
    extra = 1


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('status', 'issue', 'description')
    list_filter = ('status',)
    search_fields = ('created_at', 'edited_at', )
    inlines = [MessageInline]
    save_on_top = True
    fieldsets = (
        (None, {
            "fields": (('users', 'status', 'issue'), )
        }),
        (None, {
            "fields": ('description',)
        })
    )

    def save_model(self, request, obj, form, change):
        data = form.changed_data
        user = obj.users.filter(is_staff=False).first()
        username, email = user.username, user.email
        ticket_id = obj.id
        support = request.user.username
        if 'status' in data:
            status = data['status']
            send_mail(subject=f'Status of your ticket №{ticket_id} was changed',
                      message=f'Hello, dear {username}.'
                              f'We want you to know that {support} have changed status of your ticket to {status}.'
                              f'Best regards, CEO of GlobeMemo inc. Aleksandr Semenov',
                      from_email=None,
                      recipient_list=[email])

        super().save_model(self, request, obj, form)


admin.site.register(Message)
