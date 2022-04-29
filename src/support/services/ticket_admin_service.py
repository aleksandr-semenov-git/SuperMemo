from django.core.mail import send_mail


class TicketAdminService:
    @staticmethod
    def send_mail_change_status(ticket_id, username, support, status, email):
        """Use django.core.mail.send_mail to send email to the user. Email is about changed status"""
        send_mail(subject=f'Status of your ticket №{ticket_id} was changed. ',
                  message=f'Hello, dear {username}. '
                          f'We want you to know that {support} have changed status of your ticket to {status}. '
                          f'Best regards, CEO of GlobeMemo inc. Aleksandr Semenov. ',
                  from_email=None,
                  recipient_list=[email])
