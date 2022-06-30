from src.celery import app

from support.services.ticket_admin_service import TicketAdminService


@app.task
def celery_send_email_change_status(ticket_id, username, support, status, email):
    TicketAdminService.send_mail_change_status(ticket_id, username, support, status, email)
