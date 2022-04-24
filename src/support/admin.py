from django.contrib import admin
from support.models import Ticket, Message


class MessageInline(admin.StackedInline):
    model = Message
    extra = 1


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('status', 'issue', 'description')
    list_filter = ('status',)
    search_fields = ('created_at', 'edited_at', )
    inlines = [MessageInline]


admin.site.register(Message)
