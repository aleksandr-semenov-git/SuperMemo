from django.contrib import admin
from support.models import Ticket, Message


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
    )


admin.site.register(Message)
